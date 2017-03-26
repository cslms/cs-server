import logging
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.errors import InvalidSubmissionError, GradingError
from codeschool.lms.activities.models.mixins import HasProgressMixin, \
    subclass_registry_meta
from codeschool.lms.activities.models.submission_queryset import \
    SubmissionManager
from codeschool.lms.activities.signals import submission_graded_signal

logger = logging.getLogger('codeschool.lms.activities')

SubmissionManager.use_for_related_fields = True


class Submission(HasProgressMixin,
                 models.CopyMixin,
                 models.TimeStampedModel,
                 models.PolymorphicModel,
                 metaclass=subclass_registry_meta(type(models.PolymorphicModel))):
    """
    Represents a student's simple submission in response to some activity.
    """

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')

    progress = models.ForeignKey('Progress', related_name='submissions')
    hash = models.CharField(max_length=32, blank=True)
    ip_address = models.CharField(max_length=20, blank=True)
    num_recycles = models.IntegerField(default=0)
    feedback_class = None
    recycled = False
    objects = SubmissionManager()
    _subclass_related = ['Feedback']

    # Delegated properties
    @property
    def final_grade_pc(self):
        if self.feedback is None:
            return None
        return self.feedback.final_grade_pc

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        base = '%s by %s' % (self.activity_title, self.sender_username)
        # if self.feedback_set.last():
        #     points = self.final_feedback_pc.given_grade
        #     base += ' (%s%%)' % points
        return base

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.compute_hash()
        super().save(*args, **kwargs)

    def compute_hash(self):
        """
        Computes a hash of data to deduplicate submissions.
        """

        raise ImproperlyConfigured(
            'Submission subclass must implement the compute_hash() method.'
        )

    def autograde(self, silent=False):
        """
        Performs automatic grading and return the feedback object.

        Args:
            silent:
                Prevents the submission_graded_signal from triggering in the
                end of a successful grading.
        """

        feedback = self.feedback_class(submission=self, manual_grading=False)
        feedback.autograde()
        feedback.update_final_grade()
        feedback.save()
        self.progress.register_feedback(feedback)
        self.register_feedback(feedback)

        # Send signal
        if not silent:
            submission_graded_signal.send(Submission, submission=self,
                                          feedback=feedback, automatic=True)
        return feedback

    def register_feedback(self, feedback, commit=True):
        """
        Update itself when a new feedback becomes available.

        This method should not update the progress instance.
        """

        self.final_feedback = feedback
        if commit:
            self.save()

    def bump_recycles(self):
        """
        Increase the recycle count by one.
        """

        self.num_recycles += 1
        self.save(update_fields=['num_recycles'])

    def is_equal(self, other):
        """
        Check both submissions are equal/equivalent to each other.
        """

        if self.hash == other.hash and self.hash is not None:
            return True

        return self.submission_data() == other.submission_data()

    def submission_data(self):
        """
        Return a dictionary with data specific for submission.

        It ignores metadata such as creation and modification times, number of
        recycles, etc. This method should only return data relevant to grading
        the submission.
        """

        blacklist = {
            'id', 'num_recycles', 'ip_address', 'created', 'modified', 'hash',
            'final_feedback_id', 'submission_ptr_id', 'polymorphic_ctype_id',
        }

        def forbidden_attr(k):
            return k.startswith('_') or k in blacklist

        return {k: v for k, v in self.__dict__.items() if not forbidden_attr(k)}

    def autograde_value(self, *args, **kwargs):
        """
        This method should be implemented in subclasses.
        """

        raise ImproperlyConfigured(
            'Progress subclass %r must implement the autograde_value().'
            'This method should perform the automatic grading and return the '
            'resulting grade. Any additional relevant feedback data might be '
            'saved to the `feedback_data` attribute, which is then is pickled '
            'and saved into the database.' % type(self).__name__
        )

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

    def update_progress(self, commit=True):
        """
        Update all parameters for the progress object.

        Return True if update was required or False otherwise.
        """

        update = False
        progress = self.progress

        if self.is_correct and not progress.is_correct:
            update = True
            progress.is_correct = True

        if self.given_grade_pc > progress.best_given_grade_pc:
            update = True
            fmt = self.description, progress.best_given_grade_pc, self.given_grade_pc
            progress.best_given_grade_pc = self.given_grade_pc
            logger.info('(%s) grade: %s -> %s' % fmt)

        if progress.best_given_grade_pc > progress.grade:
            old = progress.grade
            new = progress.grade = progress.best_given_grade_pc
            logger.info(
                '(%s) grade: %s -> %s' % (progress.description, old, new))

        if commit and update:
            progress.save()

        return update

    def regrade(self, method, commit=True):
        """
        Recompute the grade for the given submission.

        If status != 'done', it simply calls the .autograde() method. Otherwise,
        it accept different strategies for updating to the new grades:
            'update':
                Recompute the grades and replace the old values with the new
                ones. Only saves the submission if the feedback_data or the
                given_grade_pc attributes change.
            'best':
                Only update if the if the grade increase.
            'worst':
                Only update if the grades decrease.
            'best-feedback':
                Like 'best', but updates feedback_data even if the grades
                change.
            'worst-feedback':
                Like 'worst', but updates feedback_data even if the grades
                change.

        Return a boolean telling if the regrading was necessary.
        """
        if self.status != self.STATUS_DONE:
            return self.autograde()

        # We keep a copy of the state, if necessary. We only have to take some
        # action if the state changes.
        def rollback():
            self.__dict__.clear()
            self.__dict__.update(state)

        state = self.__dict__.copy()
        self.autograde(force=True, commit=False)

        # Each method deals with the new state in a different manner
        if method == 'update':
            if state != self.__dict__:
                if commit:
                    self.save()
                return False
            return True
        elif method in ('best', 'best-feedback'):
            if self.given_grade_pc <= state.get('given_grade_pc', 0):
                new_feedback_data = self.feedback_data
                rollback()
                if new_feedback_data != self.feedback_data:
                    self.feedback_data = new_feedback_data
                    if commit:
                        self.save()
                    return True
                return False
            elif commit:
                self.save()
            return True

        elif method in ('worst', 'worst-feedback'):
            if self.given_grade_pc >= state.get('given_grade_pc', 0):
                new_feedback_data = self.feedback_data
                rollback()
                if new_feedback_data != self.feedback_data:
                    self.feedback_data = new_feedback_data
                    if commit:
                        self.save()
                    return True
                return False
            elif commit:
                self.save()
            return True
        else:
            rollback()
            raise ValueError('invalid method: %s' % method)

    def get_feedback_title(self):
        """
        Return the title for the feedback message.
        """

        if self.feedback is None:
            return _('Grading submission...')
        return self.feedback.get_feedback_title()


# Save a copy in the class namespace for convenience
Submission.InvalidSubmissionError = InvalidSubmissionError
