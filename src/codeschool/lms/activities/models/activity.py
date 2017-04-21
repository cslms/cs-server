import decimal
import logging

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.components.navbar import NavSection
from codeschool.lms.activities.managers.activity import ActivityManager
from codeschool.lms.activities.meta import ActivityMeta
from codeschool.lms.activities.models.utils import AuxiliaryClassIntrospection
from codeschool.types.rules import Rules

logger = logging.getLogger('codeschool.lms.activities')
ZERO = decimal.Decimal(0)


class Activity(models.ExtRoutablePage, metaclass=ActivityMeta):
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
    disabled_message = models.TextField(
        _('Disabled message'),
        blank=True,
        help_text=_(
            'Messsage explaining why the activity was disabled.'
        )
    )
    has_submissions = models.BooleanField(default=bool)
    has_correct_submissions = models.BooleanField(default=bool)
    section_title = property(lambda self: _(self._meta.verbose_name))

    objects = ActivityManager()
    rules = Rules()

    # These properties dynamically define the progress/submission/feedback
    # classes associated with the current class.
    progress_class = AuxiliaryClassIntrospection('progress')
    submission_class = AuxiliaryClassIntrospection('submission')
    feedback_class = AuxiliaryClassIntrospection('feedback')

    @property
    def submissions(self):
        return self.submission_class.objects.filter(
            progress__activity_page_id=self.id
        )

    def clean(self):
        super().clean()

        if not self.author_name and self.owner:
            name = self.owner.get_full_name()
            email = self.owner.email
            self.author_name = '%s <%s>' % (name, email)

        if self.disabled:
            raise ValidationError(self.disabled_message)

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
        logger.info('%r, submission from user %r' %
                    (self.title, user.username))
        progress = self.progress_set.for_user(user)
        return progress.submit(request, **kwargs)

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
