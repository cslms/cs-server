import decimal
import json
import logging
import os

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.components.navbar import NavSection
from codeschool.lms.activities.managers.activity import ActivityManager
from codeschool.lms.activities.meta import ActivityMeta
from codeschool.lms.activities.models.utils import get_class
from codeschool.types.rules import Rules
from codeschool.lms.activities.score_map import ScoreMap

logger = logging.getLogger('codeschool.lms.activities')
ZERO = decimal.Decimal(0)


class Activity(models.ExtRoutablePage,
               models.Page, metaclass=ActivityMeta):
    """
    Represents a gradable activity inside a course. Activities may not have an
    explicit grade, but yet may provide points to the students via the
    gamefication features of Codeschool.

    Activities can be scheduled to be done in the class or as a homework
    assignment.

    Each concrete activity is represented by a different subclass.
    """

    class Meta:
        abstract = True
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        permissions = [
            ('interact', 'Interact'),
            ('view_submissions', 'View submissions'),
        ]

    author_name = models.CharField(
        _('Author\'s name'),
        max_length=100,
        blank=True,
        help_text=_(
            'The author\'s name, if not the same user as the question owner.'
        ),
    )
    visible = models.BooleanField(
        _('Invisible'),
        default=bool,
        help_text=_(
            'Makes activity invisible to users.'
        ),
    )
    closed = models.BooleanField(
        _('Closed to submissions'),
        default=bool,
        help_text=_(
            'A closed activity does not accept new submissions, but users can '
            'see that they still exist.'
        )
    )
    group_submission = models.BooleanField(
        _('Group submissions'),
        default=bool,
        help_text=_(
            'If enabled, submissions are registered to groups instead of '
            'individual students.'
        )
    )
    max_group_size = models.IntegerField(
        _('Maximum group size'),
        default=6,
        help_text=_(
            'If group submission is enabled, define the maximum size of a '
            'group.'
        ),
    )
    disabled = models.BooleanField(
        _('Disabled'),
        default=bool,
        help_text=_(
            'Activities can be automatically disabled when Codeshool '
            'encounters an error. This usually produces a message saved on '
            'the .disabled_message attribute.'
        )
    )
    disabled_message = models.TextField(blank=True)
    has_submissions = models.BooleanField(default=bool)
    has_correct_submissions = models.BooleanField(default=bool)

    objects = ActivityManager()
    rules = Rules()

    #: Define the default material icon used in conjunction with instances of
    #: the activity class.
    personalization_default_icon = 'material:help'

    @property
    def progress_class(self):
        return get_class(self, 'progress')

    @property
    def submission_class(self):
        return get_class(self, 'submission')

    @property
    def feedback_class(self):
        return get_class(self, 'feedback')

    #: Model template
    template = 'lms/activities/activity.jinja2'

    #: Dictionary with extra static content that should be appended to the
    #: context for instances of the model.
    extra_context = {}

    __imported_data = None
    _subclass_related = ['Progress', 'Submission', 'Feedback']

    @property
    def submissions(self):
        return self.submission_class.objects.filter(
            progress__activity_page_id=self.id
        )

    @property
    def section_title(self):
        return _(self._meta.verbose_name)

    def load_post_file_data(self, file_data):
        """
        Import content from raw file data.
        """

        fmt = self.loader_format_from_filename(file_data.name)
        self.load_data(file_data, format=fmt)
        self.__imported_data = dict(self.__dict__)

        logger.info('Imported question "%s" from file "%s"' %
                    (self.title, self.import_file.name))

        # We fake POST data after loading data from file in order to make the
        # required fields validate. This part constructs a dictionary that
        # will be used to feed a fake POST data in the QuestionAdminModelForm
        # instance
        fake_post_data = {
            'title': self.title or _('Untitled'),
            'short_description': self.short_description or _('untitled'),
        }

        for field in self.OPTIONAL_IMPORT_FIELDS:
            if getattr(self, field, None):
                fake_post_data[field] = getattr(self, field)

        base_slug = slugify(fake_post_data['title'])
        auto_generated_slug = self._get_autogenerated_slug(base_slug)
        fake_post_data['slug'] = auto_generated_slug
        return fake_post_data

    def loader_format_from_filename(self, name):
        """
        Returns a string with the loader method from the file extension
        """

        _, ext = os.path.splitext(name)
        ext = ext.lstrip('.')
        return self.EXT_TO_METHOD_CONVERSIONS.get(ext, ext)

    def load_data(self, data, format='yaml'):
        """
        Load data from the given file or string object using the specified
        method.
        """

        try:
            loader = getattr(self, 'load_%s_data' % format)
        except AttributeError:
            raise ValueError('format %r is not implemented' % format)
        return loader(data)

    def clean(self):
        super().clean()

        if not self.author_name and self.owner:
            name = self.owner.get_full_name()
            email = self.owner.email
            self.author_name = '%s <%s>' % (name, email)

        if self.disabled:
            raise ValidationError(self.disabled_message)

    def full_clean(self, *args, **kwargs):
        if self.__imported_data is not None:
            blacklist = self.IMPORTED_FIELDS_BLACKLIST

            data = {k: v
                    for k, v in self.__imported_data.items()
                    if (not k.startswith('_')) and k not in blacklist and
                    v not in (None, '')}

            for k, v in data.items():
                setattr(self, k, v)

        super().full_clean(*args, **kwargs)

    def submit(self, request, user=None, **kwargs):
        """
        Create a new Submission object for the given question and saves it on
        the database.

        Args:
            request:
                The request object for the current submission.
            recycle:
                If true, recycle submission objects with the same content as the
                current submission. If a submission exists with the same content
                as the current submission, it simply returns the previous
                submission.
                If recycled, sets the submission.recycled to True.
            user:
                The user who submitted the response. If not given, uses the user
                in the request object.
        """

        if hasattr(request, 'username'):
            raise ValueError

        # Test if activity is active
        if self.closed:
            raise ValueError('activity is closed to new submissions')

        # Fetch submission class
        submission_class = self.submission_class
        if submission_class is None:
            raise ImproperlyConfigured(
                '%s must define a submission_class attribute with the '
                'appropriate submission class.' % self.__class__.__name__
            )

        # Add progress information to the given submission kwargs
        if user is None:
            user = request.user
        logger.info('%r, submission from user %r' % (self.title, user.username))
        progress = self.progress_set.for_user(user)
        return progress.submit(request, **kwargs)

    # Permissions
    def user_can_edit(self, user):
        """
        Return True if user has permissions to edit question.
        """

        return user == self.owner or user.is_superuser

    def get_statistics(self, user, **kwargs):
        """
        Return a dictionary with relevant statistics for activity.
        """

        return {
            'user_submissions': self.submissions.for_user(user).count(),
            'total_submissions': self.submissions.count(),
        }

    def get_context(self, request, *args, **kwargs):
        return dict(
            super().get_context(request, *args, **kwargs),
            activity=self,
            **self.extra_context
        )

    def best_submissions(self, context):
        """
        Return a dictionary mapping users to their best responses.
        """

        mapping = {}
        responses = self.responses.filter(context=context)
        for response in responses:
            mapping[response.user] = response.best_submission()
        return mapping

    def nav_sections(self, request):
        """
        Return a list of navigation sections for the given request.
        """

        sections = []
        default = self.nav_section_for_activity(request)
        if default.links:
            sections.append(default)
        return sections

    def nav_section_for_activity(self, request):
        """
        Return links pertinent to the activity.

        Returns:
            A NavSection instance.
        """

        nav = NavSection(self.section_title, self.get_absolute_url())
        return nav

    def users(self):
        """
        Return a queryset with all users that made a submission to the activity.
        """

        user_ids = self.responses.values_list('user', flat=True)
        users = models.User.objects.filter(id__in=user_ids)
        return users

    def score_board(self, users=None, info=None):
        """
        Return a mapping between users and their respective grades.

        Args:
            users:
                Filter users to the given set. The default behavior is to
                include all users that made any single submission.
            info ('points', 'grade', 'stars', 'score'):
                The information used to construct the score board.
        """

        info = info or 'points'
        if info not in ['points', 'grade', 'stars', 'score']:
            raise ValueError('invalid info: %r' % info)

        if users is None:
            users = self.users()

        board = ScoreMap(self.title)
        for user in users:
            response = self.responses.response_for_user(user)
            board[user] = getattr(response, info)
        return board

    def find_identical_responses(self, context, key=None, cmp=None, thresh=1):
        """
        Finds all responses with identical response_data in the set of best
        responses.

        Args:
            key:
                The result of key(response_data) is used for normalizing the
                different responses in the response set.
            cmp:
                A comparison function that take the outputs of key(x) for a
                pair of responses and return True if the two arguments are to
                be considered equal.
            thresh:
                Minimum threshold for the result of cmp(x, y) to be considered
                plagiarism.
        """

        key = key or (lambda x: x)
        responses = self.best_submissions(context).values()
        response_data = [(x, key(x.response_data))
                         for x in responses if x is not None]

        # We iterate this list in O^2 complexity by comparing every pair of
        # responses and checking if cmp(data1, data2) returns a value greater
        # than or equal thresh.
        bad_pairs = {}
        cmp = cmp or (lambda x, y: x == y)
        for i, (resp_a, key_a) in enumerate(response_data):
            for j in range(i + 1, len(response_data)):
                resp_b, key_b = response_data[j]
                value = cmp(key_a, key_b)
                if value >= thresh:
                    bad_pairs[resp_a, resp_b] = value
        return bad_pairs

    def group_identical_responses(self, context, key=None, keep_single=True):
        key = key or (lambda x: json.dumps(x))
        bad_values = {}
        for response in self.best_submissions(context).values():
            if response is None:
                continue
            key_data = key(response.response_data)
            response_list = bad_values.setdefault(key_data, [])
            response_list.append(response)

        return bad_values
