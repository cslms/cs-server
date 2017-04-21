import logging
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.lms.activities.managers.progress import ProgressManager
from codeschool.utils import get_ip

logger = logging.getLogger('codeschool.lms.activities')


class Progress(models.CopyMixin,
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

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Progress):
            if self.pk is None:
                return False
            else:
                return self.pk == other.pk
        return NotImplemented

    def submit(self, request, recycle=True, **kwargs):
        """
        Creates new submission.
        """

        submission_class = self.activity.submission_class
        submission = submission_class(progress=self, **kwargs)
        submission.ip_address = get_ip(request)

        if not recycle:
            submission.save()
            return submission

        # Collect all submissions with the same hash as current one
        recyclable = submission_class.objects\
            .filter(progress=self, hash=submission.compute_hash()) \
            .order_by('created')

        # Then check if any submission is actually equal to the current amongst
        # all candidates
        for possibly_equal in recyclable:
            if submission.is_equal(possibly_equal):
                possibly_equal.recycled = True
                possibly_equal.bump_recycles()
                return possibly_equal
        else:
            submission.save()
            return submission

    def register_feedback(self, feedback):
        """
        This method is called after a submission is graded and produces a
        feedback.
        """

        submission = feedback.submission
        self.update_grades_from_feedback(feedback)

        if not self.activity.has_submissions:
            print('first submission')
            if feedback.is_correct:
                print('first correct submission')

    def update_grades_from_feedback(self, feedback):
        """
        Update grades from the current progress object from the given feedback.
        """

        # Update grades
        if self.given_grade_pc < (feedback.given_grade_pc or 0):
            self.given_grade_pc = feedback.given_grade_pc

        # TODO: decide better update strategy
        if self.final_grade_pc < feedback.final_grade_pc:
            self.final_grade_pc = feedback.final_grade_pc

        # # Register points and stars associated with submission.
        # score_kwargs = {}
        # final_points = feedback.final_points()
        # final_stars = feedback.final_stars()
        # if final_points > self.points:
        #     score_kwargs['points'] = final_points - self.points
        #     self.points = final_points
        # if final_stars > self.stars:
        #     score_kwargs['stars'] = final_stars - self.stars
        #     self.stars = final_stars
        #
        # # If some score has changed, we save the update fields and update the
        # # corresponding UserScore object
        # if score_kwargs:
        #     from codeschool.gamification.models import UserScore
        #     self.save(update_fields=score_kwargs.keys())
        #     score_kwargs['diff'] = True
        #     UserScore.update(self.user, self.activity_page, **score_kwargs)

        # Update the is_correct field
        self.is_correct = self.is_correct or feedback.is_correct
        self.save()

    def update_from_submissions(self, grades=True, score=True, commit=True,
                                refresh=False):
        """
        Update grades and gamification scores for all submissions.

        Args:
            grades, score (bool):
                choose to update final grades and/or final scores.
            commit:
                if True (default), save changes to database.
            refresh:
                if True (default), recompute grade from scratch.
        """

        submissions = self.submissions.all()
        if refresh and submissions.count():
            first = submissions.first()
            if grades:
                self.final_grade_pc = first.given_grade_pc
                self.given_grade_pc = first.given_grade_pc
            if score:
                self.points = first.points
                self.stars = first.stars
                self.score = first.score

        for submission in submissions:
            if grades:
                submission.update_response_grades(commit=False)
            if score:
                submission.update_response_score(commit=False)

        if commit:
            self.save()

    def regrade(self, method=None, force_update=False):
        """
        Return the final grade for the user using the given method.

        If not method is given, it uses the default grading method for the
        activity.
        """

        activity = self.activity

        # Choose grading method
        if method is None and self.final_grade_pc is not None:
            return self.final_grade_pc
        elif method is None:
            grading_method = activity.grading_method
        else:
            grading_method = GradingMethod.from_name(activity.owner, method)

        # Grade response. We save the result to the final_grade_pc attribute if
        # no explicit grading method is given.
        grade = grading_method.grade(self)
        if method is None and (force_update or self.final_grade_pc is None):
            self.final_grade_pc = grade
        return grade
