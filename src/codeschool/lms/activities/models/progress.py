import logging
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.utils.request import get_ip
from .mixins import CommitMixin
from ..managers.progress import ProgressManager

logger = logging.getLogger('codeschool.lms.activities')


class Progress(CommitMixin,
               models.CopyMixin,
               models.StatusModel,
               models.TimeStampedModel,
               models.PolymorphicModel):
    """
    When an user starts an activity it opens a Progress object which control
    all submissions to the given activity.

    The Progress object also manages individual submissions that may span
    several http requests.
    """

    class Meta:
        unique_together = [('user', 'activity_page')]
        verbose_name = _('student progress')
        verbose_name_plural = _('student progress list')

    STATUS_OPENED = 'opened'
    STATUS_CLOSED = 'closed'
    STATUS_INCOMPLETE = 'incomplete'
    STATUS_WAITING = 'waiting'
    STATUS_INVALID = 'invalid'
    STATUS_DONE = 'done'

    STATUS = models.Choices(
        (STATUS_OPENED, _('opened')),
        (STATUS_CLOSED, _('closed')),
    )

    user = models.ForeignKey(models.User, on_delete=models.CASCADE)
    activity_page = models.ForeignKey(models.Page, on_delete=models.CASCADE)
    final_grade_pc = models.DecimalField(
        _('final score'),
        max_digits=6, decimal_places=3, default=Decimal,
        help_text=_(
            'Final grade given to considering all submissions, penalties, etc.'
        ),
    )
    given_grade_pc = models.DecimalField(
        _('grade'),
        max_digits=6, decimal_places=3, default=Decimal,
        help_text=_('Final grade before applying any modifier.'),
    )
    finished = models.DateTimeField(blank=True, null=True)
    best_submission = models.ForeignKey('Submission', blank=True, null=True,
                                        related_name='+')
    points = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    stars = models.FloatField(default=0.0)
    is_correct = models.BooleanField(default=bool)
    has_submissions = models.BooleanField(default=bool)
    has_feedback = models.BooleanField(default=bool)
    has_post_tests = models.BooleanField(default=bool)
    objects = ProgressManager()

    #: The number of submissions
    num_submissions = property(lambda x: x.submissions.count())

    #: Specific activity reference
    activity = property(lambda x: x.activity_page.specific)
    activity_id = property(lambda x: x.activity_page_id)

    #: Has progress mixin interface
    username = property(lambda x: x.user.username)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        tries = self.num_submissions
        user = self.user
        activity = self.activity
        grade = '%s pts' % (self.final_grade_pc or 0)
        fmt = '%s by %s (%s, %s tries)'
        return fmt % (activity, user, grade, tries)

    def submit(self, request, payload, recycle=True, commit=True):
        """
        Creates new submission.

        Args:
            recycle:
                If True, recycle submission objects with the same content as the
                current submission. If a submission exists with the same content
                as the current submission, it simply returns the previous
                submission. If recycled, sets the submission.recycled to True.
        """

        submission_class = self.activity.submission_class
        submission = submission_class(progress=self, **payload)
        submission.ip_address = get_ip(request)
        submission.hash = submission.compute_hash()
        submission.full_clean()

        # Then check if any submission is equal to some past submission and
        # then recycle it
        recyclable = submission_class.objects.recyclable(submission)
        recyclable = recyclable if recycle else ()
        for possibly_equal in recyclable:
            if submission.is_equal(possibly_equal):
                possibly_equal.recycled = True
                possibly_equal.bump_recycles()
                return possibly_equal
        else:
            return submission.commit(commit)

    def register_feedback(self, feedback, commit=True):
        """
        This method is called after a submission is graded and produces a
        feedback.
        """

        submission = feedback.submission

        # Check if it is the best submission
        grade = feedback.given_grade_pc
        if (self.best_submission is None or
                self.best_submission.feedback.given_grade_pc < grade):
            self.best_submission = submission

        # Update grades for activity considering past submissions
        self.update_grades_from_feedback(feedback)
        self.commit(commit)

    def update_grades_from_feedback(self, feedback):
        """
        Update grades from the current progress object from the given feedback.
        """

        # Update grades, keeping always the best grade
        if self.given_grade_pc < (feedback.given_grade_pc or 0):
            self.given_grade_pc = feedback.given_grade_pc
        if self.final_grade_pc < feedback.final_grade_pc:
            self.final_grade_pc = feedback.final_grade_pc

        # Update the is_correct field
        self.is_correct = self.is_correct or feedback.is_correct
