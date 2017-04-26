from codeschool.questions.models import QuestionProgress
from codeschool.utils.managers import manager_instance, queryset_class


class CodingIoProgessQuerySet(queryset_class(QuestionProgress)):

    def regrade_with(self, tests, **kwargs):
        """
        Recompute progress grades with the given tests.

        Args:
            tests (iospec):
                New tests to check all submissions against.

        Returns:
            A tuple with the # of changed submissions and the total # of
            regraded submissions.

        """

        total = 0
        changed = 0
        for response in self.all():
            total += 1
            ch, _ = response.regrade(tests, **kwargs)
            changed += bool(ch)
        return changed, total


class CodingIoProgress(QuestionProgress):
    """
    Progress type for CodingIoQuestion's.
    """

    objects = manager_instance(QuestionProgress, CodingIoProgessQuerySet,
                               use_for_related_fields=True)

    def post_grading(self, tests=None, **kwargs):
        """
        Regrade response using the given set of tests.

        Args:
            tests (IoSpec):
                New tests to check all submissions against.
        """

        if tests is None:
            tests = self.question.post_tests_expanded

        total = 0
        changed = 0
        for submission in self.submissions.all():
            total += 1
            changed += submission.run_post_grading(tests, **kwargs)

        values = self.submissions.values_list('final_grade', 'given_grade')
        self.final_grade = max(x for x, y in values)
        self.given_grade = max(y for x, y in values)
        self.is_correct = self.submissions.has_correct()
        self.save()
