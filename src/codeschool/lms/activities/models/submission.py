import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.errors import InvalidSubmissionError, GradingError
from codeschool.utils.misc import update_state
from codeschool.utils.string import md5hash
from .mixins import FromProgressAttributesMixin, CommitMixin
from ..managers.submission import SubmissionManager
from ..signals import submission_graded_signal

logger = logging.getLogger('codeschool.lms.activities')


class Submission(CommitMixin,
                 FromProgressAttributesMixin,
                 models.CopyMixin,
                 models.TimeStampedModel,
                 models.PolymorphicModel):
    """
    Represents a student's simple submission in response to some activity.
    """

    progress = models.ForeignKey('Progress', related_name='submissions')
    hash = models.CharField(max_length=32)
    ip_address = models.CharField(max_length=20, blank=True)
    num_recycles = models.IntegerField(default=0)
    recycled = False

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')

    # Properties
    has_feedback = property(lambda self: hasattr(self, 'feedback'))
    objects = SubmissionManager()

    # Delegated properties
    @property
    def final_grade_pc(self):
        if self.has_feedback:
            return None
        return self.feedback.final_grade_pc

    @property
    def feedback_class(self):
        name = self.__class__.__name__.replace('Submission', 'Feedback')
        return apps.get_model(self._meta.app_label, name)

    @classmethod
    def data_fields(cls):
        """
        Return a list of attributes that store submission data.

        It ignores metadata such as creation and modification times, number of
        recycles, etc. This method should only return fields relevant to grading
        the submission.
        """

        blacklist = {
            'id', 'num_recycles', 'ip_address', 'created', 'modified', 'hash',
            'final_feedback_id', 'submission_ptr_id', 'polymorphic_ctype_id',
            'progress_id',
        }

        fields = [field.attname for field in cls._meta.fields]
        return [field for field in fields if field not in blacklist]

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        username = self.user.username
        base = '%s by %s' % (self.activity_title, username)
        return base

    def clean(self):
        if not self.hash:
            self.hash = self.compute_hash()
        super().clean()

    def compute_hash(self):
        """
        Computes a hash of data to deduplicate submissions.
        """

        fields = get_default_fields(type(self))
        return md5hash(';'.join(map(lambda f: str(getattr(self, f)), fields)))

    def auto_feedback(self, silent=False, commit=True):
        """
        Performs automatic grading and return the feedback object.

        Args:
            silent:
                Prevents the submission_graded_signal from triggering in the
                end of a successful grading.
        """

        # Create feedback object
        feedback = self.feedback_class(submission=self, manual_grading=False)
        feedback.given_grade_pc, state = feedback.get_autograde_value()
        feedback.is_correct = feedback.given_grade_pc == 100
        update_state(feedback, state)
        feedback.final_grade_pc = feedback.get_final_grade_value()
        feedback.commit(commit)

        # Register graded feedback
        self.register_feedback(feedback)

        # Send signal
        if not silent:
            submission_graded_signal.send(Submission, submission=self,
                                          feedback=feedback, automatic=True)
        return feedback

    def is_equal(self, other):
        """
        Check both submissions are equal/equivalent to each other.
        """

        if self.hash != other.hash and self.hash and other.hash:
            return False

        fields = get_default_fields(type(self))
        return all(getattr(self, f) == getattr(other, f) for f in fields)

    def bump_recycles(self):
        """
        Increase the recycle count by one.
        """

        self.num_recycles += 1
        self.save(update_fields=['num_recycles'])

    def register_feedback(self, feedback, commit=True):
        """
        Update itself when a new feedback becomes available.

        This method should not update the progress instance.
        """

        # Call the register feedback of the progress object
        self.progress.register_feedback(feedback)

    def manual_grade(self, grade, commit=True, raises=False, silent=False):
        """
        Saves result of manual grading.

        Args:
            grade (number):
                Given grade, as a percentage value.
            commit:
                If false, prevents saving the object when grading is complete.
                The user must save the object manually after calling this
                method.
            raises:
                If submission has already been graded, raises a GradingError.
            silent:
                Prevents the submission_graded_signal from triggering in the
                end of a successful grading.
        """

        if self.status != self.STATUS_PENDING and raises:
            raise GradingError(
                'Submission has already been graded!'
            )

        raise NotImplementedError('TODO')

    def get_feedback_title(self):
        """
        Return the title for the feedback message.
        """

        try:
            feedback = self.feedback
        except AttributeError:
            return _('Not graded')
        else:
            return feedback.get_feedback_title()


def get_default_fields(cls):
    """
    Return the default field names for class.
    """

    try:
        fields = cls._meta.data_fields
    except AttributeError:
        cls._meta.data_fields = fields = cls.data_fields()
    return fields


# Save a copy in the class namespace for convenience
Submission.InvalidSubmissionError = InvalidSubmissionError
