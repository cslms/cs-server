from django.db import models
from django.utils.translation import ugettext_lazy as _

from codeschool.questions.models import Question, QuestionProgress, \
    QuestionSubmission, QuestionFeedback
from .grader import code_errors


class CodeQuestion(Question):
    """
    Grade a question by comparing the student's implementation with a reference
    implementation and some examples.
    """

    grader = models.TextField(
        _('Grader source code'),
        help_text=_(
            'The grader is a Python script that defines a '
            '"grade(test, reference)" function that takes the test function '
            'and a reference implementation and raise AssertionErrors if '
            'something fail.'
        ),
    )
    reference = models.TextField(
        _('Reference implementation'),
        help_text=_(
            'Reference implementation for the correct function.'
        ),
    )
    function_name = models.CharField(
        _('Function name'),
        max_length=80,
        default='func',
        help_text=_(
            'The name of the test object. (This is normally a function, but '
            'we can also test classes, data structures, or anything)',
        ),
    )
    timeout = models.FloatField(
        _('Timeout'),
        default=1.0,
        help_text=_(
            'Maximum interval (in seconds) used to grade the question.'
        ),
    )


class CodeQuestionProgress(QuestionProgress):
    """
    Progress object for code questions.
    """


class CodeQuestionSubmission(QuestionSubmission):
    """
    Submission object for code questions.
    """

    source = models.TextField()


class CodeQuestionFeedback(QuestionFeedback):
    """
    Feedback object for code questions.
    """

    error_message = models.TextField()


def find_code_errors(question, code):
    """
    Return an error message for any defects encountered on the given string
    of python code.
    """

    import boxed
    names = [x.strip() for x in question.names.split(',')]

    return boxed.run(code_errors,
                     args=(question.grader, code, question.reference),
                     kwargs={'name': question.function_name},
                     timeout=question.timeout,
                     method='json')
