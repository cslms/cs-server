import decimal
import logging

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.types.rules import Rules
from .mixins import CommitMixin
from .utils import AuxiliaryClassIntrospection
from ..managers.activity import ActivityManager
from ..meta import ActivityMeta

logger = logging.getLogger('codeschool.lms.activities')
ZERO = decimal.Decimal(0)


def bool_to_true():
    return True


class Activity(CommitMixin,
               models.RoutableViewsPage,
               models.DecoupledAdminPage,
               metaclass=ActivityMeta):
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
    # Do we need this? Can we use wagtail's live attribute?
    visible = models.BooleanField(
        _('Invisible'),
        default=bool_to_true,
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
            'the .disabled_message attribute. '
            'This field is not controlled directly by users.'
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

    def disable(self, error_message=_('Internal error'), commit=True):
        """
        Disable activity.

        Args:
            message:
                An error message explaining why activity was disabled.
        """

        self.disabled = True
        self.disabled_message = error_message
        self.commit(commit, update_fields=['disabled', 'disabled_message'])

    def submit(self, request, _commit=True, **kwargs):
        """
        Create a new Submission object for the given question and saves it on
        the database.

        Args:
            request:
                The request object for the current submission. The user is
                obtained from the request object.

        This code loads the :cls:`Progress` object for the given user and
        calls it :meth:`Progress.submit`` passing all named arguments to it.

        Subclasses should personalize the submit() method of the Progress object
        instead of the one in this class.
        """

        assert hasattr(request, 'user'), 'request do not have a user attr'

        # Test if activity is active
        if self.closed or self.disabled:
            raise RuntimeError('activity is closed to new submissions')

        # Fetch submission class
        submission_class = self.submission_class
        if submission_class is None:
            raise ImproperlyConfigured(
                '%s must define a submission_class attribute with the '
                'appropriate submission class.' % self.__class__.__name__
            )

        # Dispatch to the progress object
        user = request.user
        logger.info('%r, submission from user %r' %
                    (self.title, user.username))
        progress = self.progress_set.for_user(user)
        return progress.submit(request, kwargs, commit=_commit)

    def filter_user_submission_payload(self, request, payload):
        """
        Filter a dictionary of arguments supplied by an user and return a
        dictionary with only those arguments that should be passed to the
        .submit() function.
        """

        data_fields = self.submission_class.data_fields()
        return {k: v for (k, v) in payload.items() if k in data_fields}

    def submit_with_user_payload(self, request, payload):
        """
        Return a submission from a dictionary of user provided kwargs.

        It first process the keyword arguments and pass them to the .submit()
        method.
        """

        payload = self.filter_user_submission_payload(request, payload)
        return self.submit(request, **payload)
