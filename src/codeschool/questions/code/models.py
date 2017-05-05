from django.db import models
from django.utils.translation import ugettext_lazy as _

from bricks.html5 import div, h2, p, pre
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

    def serve_ajax_submission(self, client, source=None, **kwargs):
        """
        Handles student responses via AJAX and a bricks program.
        """

        if source is None:
            client.dialog(
                div()[
                    h2(_('Error')),
                    p(class_='dialog-text')[_('Cannot send empty submissions.')]
                ]
            )

        return super().serve_ajax_submission(
            client=client,
            source=source,
        )


class CodeProgress(QuestionProgress):
    """
    Progress object for code questions.
    """


class CodeSubmission(QuestionSubmission):
    """
    Submission object for code questions.
    """

    source = models.TextField(blank=False)


class CodeFeedback(QuestionFeedback):
    """
    Feedback object for code questions.
    """

    error_message = models.TextField(blank=True)

    def get_autograde_value(self):
        question = self.question
        submission = self.submission

        source = submission.source
        error = find_code_errors(question, source)
        return 100 if error is None else 0, {'error_message': error or ''}

    def render_message(self):
        if self.is_correct:
            return super().render_message()
        return \
            div()[
                pre(self.error_message)
            ]


def find_code_errors(question, code, use_sandbox=True):
    """
    Return an error message for any defects encountered on the given string
    of python code.
    """

    args = (question.grader, code, question.reference, question.function_name)
    runner = lambda f, args, **kwargs: f(*args)

    if use_sandbox:
        import boxed

        runner = boxed.run

    return \
        runner(code_errors,
               args=args,
               serializer='json',
               timeout=question.timeout,
               imports=['codeschool.questions.code.boxed_imports'])
