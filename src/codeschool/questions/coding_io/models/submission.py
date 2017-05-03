import json

from codeschool import models
from codeschool.questions.models import QuestionSubmission
from codeschool.utils.managers import manager_instance, queryset_class
from codeschool.utils.string import md5hash


class CodingIoSubmissionQuerySet(queryset_class(QuestionSubmission)):

    def best_code_for_user(self, user, attrs=None, activity=None):
        """
        Return the code for the best submission for the given user.

        If no submission is found, return None.
        """

        submission = self.best_for_user(user, attrs, activity=activity)
        if submission is None:
            return None
        return submission.source

    def best_code_for_users(self, attrs=None, activity=None):
        """
        Return a dictionary with source code from the best submission by each
        user.
        """

        def source(data):
            return json.loads(data)['source']

        best = self.best_for_users(attrs, activity=activity)
        return {user: submission.source for user, submission in best.items()}


class CodingIoSubmission(QuestionSubmission):
    """
    A response proxy class specialized in CodingIoQuestion responses.
    """

    source = models.TextField(blank=True)
    language = models.ForeignKey('core.ProgrammingLanguage')

    objects = manager_instance(QuestionSubmission, CodingIoSubmissionQuerySet,
                               use_for_related_fields=True)
