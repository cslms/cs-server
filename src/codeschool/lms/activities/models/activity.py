import decimal
import json
import logging
import os

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.models.base import ModelBase
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from lazyutils import lazy_classattribute, lazy

import srvice
from wagtail.wagtailcore.models import PageBase

from codeschool import blocks
from codeschool import models
from codeschool import panels
from codeschool.components.navbar import NavSection
from codeschool.lms.activities.models import subclass_registry_meta
from codeschool.lms.activities.score_map import ScoreMap

logger = logging.getLogger('codeschool.lms.activities')
ZERO = decimal.Decimal(0)
RESOURCE_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('image', blocks.ImageChooserBlock()),
    ('embed', blocks.EmbedBlock()),
    # ('markdown', blocks.MarkdownBlock()),
    ('url', blocks.URLBlock()),
    ('text', blocks.TextBlock()),
    ('char', blocks.CharBlock()),
    # ('ace', blocks.AceBlock()),
    ('bool', blocks.BooleanBlock()),
    ('doc', blocks.DocumentChooserBlock()),
    # ('snippet', blocks.SnippetChooserBlock(GradingMethod)),
    ('date', blocks.DateBlock()),
    ('time', blocks.TimeBlock()),
    ('stream', blocks.StreamBlock([
        ('page', blocks.PageChooserBlock()),
        ('html', blocks.RawHTMLBlock())
    ])),
]


class ActivityQueryset(models.PageQuerySet):
    def auth(self, user, role=None):
        """
        Filter only activities that the user can see.
        """

        return self.filter(live=True)

    def from_file(self, path, parent=None):
        """
        Creates a new object from file path.
        """

        return self.model.load_from_file(path, parent)


ActivityManager = models.PageManager.from_queryset(ActivityQueryset)


class Meta:
    """
    A internal class that have all activity meta fields and their default
    values.
    """

    #: Defines if activity allows automatic grading
    automatic_grading = True

    #: True for activities that do not allow instant feedback
    instant_feedback = True


@subclass_registry_meta
class ActivityMeta(PageBase):
    """
    Metaclass for Activity
    """

    CONCRETE_ACTIVITY_TYPES = []
    META_VARS = (attr for attr in dir(Meta) if not attr.startswith('_'))
    META_VARS = {attr: getattr(Meta, attr) for attr in META_VARS}

    def __init__(cls, name, bases, namespace):
        # Extract additional fields before intializing the metaclass
        meta = namespace.pop('Meta', None)
        if meta is not None:
            fields, meta = cls._extract_meta_fields(meta)
            namespace['Meta'] = meta
        else:
            fields = {}
        super().__init__(name, bases, namespace)

        # Register extra fields
        for attr, value in fields.items():
            setattr(cls._meta, attr, value)

    def _extract_meta_fields(self, meta):
        """
        Takes a Meta class and return a tuple (fields, Meta) with the activity
        fields extracted from Meta and a new Meta class that can be passed to
        Django.
        """

        vars = {attr: getattr(meta, attr, None) for attr in dir(meta)}
        fields = {k: v for k, v in vars.items() if k in self.META_VARS}
        fields = dict(self.META_VARS, **fields)
        vars = {k: v for k, v in vars.items() if k not in self.META_VARS}
        meta = type('Meta', (), vars)
        return fields, meta


class Activity(models.RoutablePageMixin, models.Page, metaclass=ActivityMeta):
    """
    Represents a gradable activity inside a course. Activities may not have an
    explicit grade, but yet may provide points to the students via the
    gamefication features of Codeschool.

    Activities can be scheduled to be done in the class or as a homework
    assignment.

    Each concrete activity is represented by a different subclass.
    """

    EXT_TO_METHOD_CONVERSIONS = {}
    IMPORTED_FIELDS_BLACKLIST = {
        # References
        'id', 'owner_id', 'page_ptr_id', 'content_type_id',

        # Saved fields
        'title', 'short_description', 'seo_title', 'author_name',
        'slug', 'comments', 'score_value', 'stars_value', 'difficulty',

        # Forbidden fields
        'import_file',

        # Wagtail specific fields
        'path', 'depth', 'url_path', 'numchild', 'go_live_at',
        'expire_at', 'show_in_menus', 'has_unpublished_changes',
        'latest_revision_created_at', 'first_published_at',
        'live', 'expired', 'locked',
        'search_description',
    }

    class Meta:
        abstract = True
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

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

    #: Define the default material icon used in conjunction with instances of
    #: the activity class.
    personalization_default_icon = 'material:help'

    #: The response class associated with the given activity.
    submission_class = None

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
        return _(self.__class__.__name__)

    @lazy
    def actions(self):
        return [attr[7:] for attr in dir(self) if attr.startswith('action_')]

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
        try:
            submission_class = type(self).__dict__['submission_class']
        except KeyError:
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

    # def process_response_item(self, response, recycled=False):
    #     """
    #     Process this response item generated by other activities using a context
    #     that you own.
    #
    #     This might happen in compound activities like quizzes, in which the
    #     response to a question uses a context own by a quiz object. This
    #     function allows the container object to take any additional action
    #     after the response is created.
    #     """
    #
    # def has_response(self, user=None, context=None):
    #     """
    #     Return True if the user has responded to the activity.
    #     """
    #
    #     response = self.get_response(user, context)
    #     return response.response_items.count() >= 1
    #
    # def correct_responses(self, context=None):
    #     """
    #     Return a queryset with all correct responses for the given context.
    #     """
    #
    #     done = apps.get_model('cs_core', 'ResponseItem').STATUS_DONE
    #     items = self.response_items(context, status=done)
    #     return items.filter(given_grade=100)
    #
    # def import_responses_from_context(self, from_context, to_context,
    #                                   user=None,
    #                                   discard=False):
    #     """
    #     Import all responses associated with `from_context` to the `to_context`.
    #
    #     If discard=True, responses in the original context are discarded.
    #     """
    #
    #     if from_context == to_context:
    #         raise ValueError('contexts cannot be the same')
    #
    #     responses = self.response_items(user=user, context=from_context)
    #     for response_item in responses:
    #         old_response = response_item.response
    #         new_response = self.get_response(context=to_context,
    #                                          user=old_response.user)
    #         if not discard:
    #             response_item.pk = None
    #         response_item.response = new_response
    #         response_item.save()
    #
    # # Serving pages
    # def response_context_from_request(self, request):
    #     """
    #     Return the context from the request object.
    #     """
    #
    #     try:
    #         context_pk = request.GET['context']
    #         objects = apps.get_model('cs_core', 'ResponseContext').objects
    #         return objects.get(pk=context_pk)
    #     except KeyError:
    #         return self.default_context

    def get_statistics(self, user, **kwargs):
        """
        Return a dictionary with relevant statistics for activity.
        """

        return {
            'user_submissions': self.submissions.for_user(user).count(),
            'total_submissions': self.submissions.count(),
            'total_responses': self.responses.count(),
            'total_correct': self.responses.correct().count(),
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

    # def get_user_response(self, user, method='first'):
    #     """
    #     Return some response given by the user or None if the user has not
    #     responded.
    #
    #     Allowed methods:
    #         unique:
    #             Expects that response is unique and return it (or None).
    #         any:
    #             Return a random user response.
    #         first:
    #             Return the first response given by the user.
    #         last:
    #             Return the last response given by the user.
    #         best:
    #             Return the response with the best final grade.
    #         worst:
    #             Return the response with the worst final grade.
    #         best-given:
    #             Return the response with the best given grade.
    #         worst-given:
    #             Return the response with the worst given grade.
    #
    #     """
    #
    #     responses = self.responses.filter(user=user)
    #     first = lambda x: x.select_subclasses().first()
    #
    #     if method == 'unique':
    #         N = self.responses.count()
    #         if N == 0:
    #             return None
    #         elif N == 1:
    #             return response.select_subclasses().first()
    #         else:
    #             raise ValueError(
    #                 'more than one response found for user %r' % user.username
    #             )
    #     elif method == 'any':
    #         return first(responses)
    #     elif method == 'first':
    #         return first(responses.order_by('created'))
    #     elif method == 'last':
    #         return first(responses.order_by('-created'))
    #     elif method in ['best', 'worst', 'best-given', 'worst-given']:
    #         raise NotImplementedError(
    #             'method = %r is not implemented yet' % method
    #         )
    #     else:
    #         raise ValueError('invalid method: %r' % method)
    #
    # def autograde_all(self, force=False, context=None):
    #     """
    #     Grade all responses that had not been graded yet.
    #
    #     This function may take a while to run, locking the server. Maybe it is
    #     a good idea to run it as a task or in a separate thread.
    #
    #     Args:
    #         force (boolean):
    #             If True, forces the response to be re-graded.
    #     """
    #
    #     # Run autograde on each responses
    #     for response in responses:
    #         response.autograde(force=force)
    #
    # def select_users(self):
    #     """
    #     Return a queryset with all users that responded to the activity.
    #     """
    #
    #     user_ids = self.responses.values_list('user', flat=True).distinct()
    #     users = models.User.objects.filter(id__in=user_ids)
    #     return users
    #
    # def get_grades(self, users=None):
    #     """
    #     Return a dictionary mapping each user to their respective grade in the
    #     activity.
    #
    #     If a list of users is given, include only the users in this list.
    #     """
    #
    #     if users is None:
    #         users = self.select_users()
    #
    #     grades = {}
    #     for user in users:
    #         grade = self.get_user_grade(user)
    #         grades[user] = grade
    #     return grades

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

    @srvice.route(r'^action/$')
    def serve_action(self, client, name, *args, **kwargs):
        method = getattr(self, 'action_' + name)
        return method(client, *args, **kwargs)

    def action_close(self, client):
        if client.user == self.owner:
            self.closed = True
            self.save()
        else:
            raise ValueError('only owner can close activity')

    def action_show_grades(self, client):
        grades = self.score_board()
        grades.sort()
        client.dialog(html=grades.__html__())

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

    #
    # Statistics
    #
    def response_items(self, context=None, status=None, user=None):
        """
        Return a queryset with all response items associated with the given
        activity.

        Can filter by context, status and user
        """

        items = self.response_item_class.objects
        queryset = items.filter(response__activity_id=self.id)

        # Filter context
        if context != 'any':
            context = context or self.context
            queryset = queryset.filter(response__context_id=context.id)

        # Filter user
        user = user or self.user
        if user:
            queryset = queryset.filter(response__user_id=user.id)

        # Filter by status
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def _stats(self, attr, context, by_item=False):
        if by_item:
            items = self.response_items(context, self.STATUS_DONE)
            values_list = items.values_list(attr, flat=True)
            return Statistics(attr, values_list)
        else:
            if context == 'any':
                items = self.responses.all()
            else:
                context = context or self.context
                items = self.responses.all().filter(context=context)
            return Statistics(attr, items.values_list(attr, flat=True))

    def best_final_grade(self, context=None):
        """
        Return the best final grade given for this activity.
        """

        return self._stats('final_grade', context).max()

    def best_given_grade(self, context=None):
        """
        Return the best grade given for this activity before applying any
        penalties and bonuses.
        """

        return self._stats('given_grade', context).min()

    def mean_final_grade(self, context=None, by_item=False):
        """
        Return the average value for the final grade for this activity.

        If by_item is True, compute the average over all response items instead
        of using the responses for each student.
        """

        return self._stats('final_grade', context, by_item).mean()

    def mean_given_grade(self, by_item=False):
        """
        Return the average value for the given grade for this activity.
        """

        return self._stats('given_grade', context, by_item).mean()

    # Permissions
    def can_edit(self, user):
        """
        Return True if user has permissions to edit activity.
        """

        return user == self.owner or self.course.can_edit(user)

    def can_view(self, user):
        """
        Return True if user has permission to view activity.
        """

        course = self.course
        return (
            self.can_edit(user) or
            user in course.students.all() or
            user in self.staff.all()
        )

    # Wagtail admin
    # subpage_types = []
    # parent_page_types = []
    # content_panels = models.Page.content_panels + [
    #    panels.MultiFieldPanel([
    #        # panels.RichTextFieldPanel('short_description'),
    #    ], heading=_('Options')),
    # ]
    # promote_panels = models.Page.promote_panels + [
    #    panels.FieldPanel('icon_src')
    # ]
    #settings_panels = models.Page.settings_panels + [
    #    panels.MultiFieldPanel([
    #        panels.FieldPanel('points_total'),
    #        panels.FieldPanel('stars_total'),
    #    ], heading=_('Scores'))
    #]


class ScoreDescriptor:
    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        return ScoreHandler(obj)


class ScoreHandler:
    """
    Implements the "Activity.score" property.

    This is a manager-like object that handles points and stars associated to an
    activity.
    """

    def __init__(self, instance):
        self.instance = instance

    @lazy_classattribute
    def _user_score(self):
        from codeschool.gamification.models import UserScore
        return UserScore

    @lazy_classattribute
    def _total_score(self):
        from codeschool.gamification.models import TotalScore
        return TotalScore

    def points(self, user):
        """
        Number of points associated to user.
        """

        return self._user_score.load(user, self.instance).points

    def stars(self, user):
        """
        Stars associated to user.
        """

        return self._user_score.load(user, self.instance).stars

    def points_total(self):
        """
        Return the total number of points associated with activity.
        """

        if self.instance.num_child == 0:
            return self.instance.points_total
        return self._total_score.load(self.instance).points

    def stars_total(self):
        """
        Return the total number of stars associated with activity.
        """

        if self.instance.num_child == 0:
            return self.instance.stars_total
        return self._total_score.load(self.instance).stars


Activity.score = ScoreDescriptor()
