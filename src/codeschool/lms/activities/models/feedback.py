from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from lazyutils import lazy

from bricks.html5 import p
from codeschool import models
from .mixins import FromProgressAttributesMixin, CommitMixin
from ..validators import grade_validator


class Feedback(CommitMixin,
               FromProgressAttributesMixin,
               models.TimeStampedModel,
               models.PolymorphicModel):
    """
    Feedback for user.

    Usually there will be one feedback per submission, but this figure may
    vary from case to case.
    """
    TITLE_OK = _('Correct answer!')
    TITLE_PARTIAL = _('Partially correct.')
    TITLE_WRONG = _('Wrong answer.')
    TITLE_NOT_GRADED = _('Not graded.')

    MESSAGE_OK = _(
        '*Congratulations!* Your response is correct!'
    )
    MESSAGE_OK_WITH_PENALTIES = _(
        'Your response is correct, but you did not achieved the maximum grade.'
    )
    MESSAGE_WRONG = _(
        'I\'m sorry. Wrong response response!'
    )
    MESSAGE_PARTIAL = _(
        'Your answer is partially correct: you achieved %(grade)d%% of '
        'the total grade.'
    )
    MESSAGE_NOT_GRADED = _(
        'Your response has not been graded yet!'
    )

    submission = models.OneToOneField('Submission', related_name='feedback')
    manual_grading = models.BooleanField(
        default=True,
        help_text=_(
            'True if feedback was created manually by a human.'
        )
    )
    grader_user = models.ForeignKey(
        models.User, blank=True, null=True,
        help_text=_(
            'User that performed the manual grading.'
        )
    )
    given_grade_pc = models.DecimalField(
        _('percentage of maximum grade'),
        help_text=_(
            'This grade is given by the auto-grader and represents the grade '
            'for the response before accounting for any bonuses or penalties.'
        ),
        max_digits=6,
        decimal_places=3,
        validators=[grade_validator],
        blank=True,
        null=True,
    )
    final_grade_pc = models.DecimalField(
        _('final grade'),
        help_text=_(
            'Similar to given_grade, but can account for additional factors '
            'such as delay penalties or for any other reason the teacher may '
            'want to override the student\'s grade.'
        ),
        max_digits=6,
        decimal_places=3,
        validators=[grade_validator],
        blank=True,
        null=True,
    )
    is_correct = models.BooleanField(default=False)
    progress = lazy(lambda x: x.submission.progress)

    def get_feedback_title(self):
        """
        Return a title summarizing the feedback result. The default set of
        titles come from the list:

            * Correct answer!
            * Partially correct.
            * Wrong answer.
            * Not graded.

        Different question types may define additional values to this list.
        """

        grade = self.given_grade_pc

        if grade == 100:
            return self.TITLE_OK
        elif grade is not None and grade > 0:
            return self.TITLE_PARTIAL
        elif grade == 0:
            return self.TITLE_WRONG
        else:
            return self.TITLE_NOT_GRADED

    def get_autograde_value(self):
        """
        Return the (given_grade_pc value, field_updates) for the current
        submission.

        The second parameter is a dictionary with all fields that should be
        updated in the feedback model.

        Returns:
            A numeric value between 0 and 100 with the assigned grade.
        """

        name = self.__class__.__name__
        raise ImproperlyConfigured(
            'Class %s must implement the .get_autograde_value() method.' % name
        )

    def get_final_grade_value(self):
        """
        Compute and return the final grade applying all possible penalties and
        bonuses.
        """

        return self.given_grade_pc

    def render_message(self, **kwargs):
        """
        Renders feedback message.
        """

        if self.is_correct and self.final_grade_pc >= self.given_grade_pc:
            msg = self.MESSAGE_OK
        elif self.is_correct and self.final_grade_pc < self.given_grade_pc:
            msg = self.MESSAGE_OK_WITH_PENALTIES
        elif not self.is_correct and self.given_grade_pc > 0:
            msg = self.MESSAGE_PARTIAL
        else:
            msg = self.MESSAGE_WRONG
        return p(msg, cls='cs-feedback-message').render(**kwargs)
