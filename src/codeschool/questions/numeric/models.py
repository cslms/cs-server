from django import forms
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.questions.models import Question, QuestionFeedback, \
    QuestionSubmission, QuestionProgress


class NumericQuestion(Question):
    """
    A very simple question with a simple numeric answer.
    """

    correct_answer = models.FloatField(
        _('Correct answer'),
        help_text=_(
            'The expected numeric answer for question.'
        )
    )

    tolerance = models.FloatField(
        _('Tolerance'),
        default=0,
        help_text=_(
            'If tolerance is zero, the responses must be exact.'
        ),
    )
    label = models.CharField(
        _('Label'),
        max_length=100,
        default=_('Answer'),
        help_text=_(
            'The label text that is displayed in the submission form.'
        ),
    )
    help_text = models.TextField(
        _('Help text'),
        blank=True,
        help_text=_(
            'Additional explanation that is displayed under the input form.'
        )
    )

    class Meta:
        verbose_name = _('Numeric question')
        verbose_name_plural = _('Numeric questions')

    def get_form_class(self):
        class NumericForm(forms.Form):
            value = forms.FloatField(label=self.label, required=True)

        return NumericForm

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(*args, **kwargs)

    # Serving Pages
    template = 'questions/numeric/detail.jinja2'

    def get_context(self, request, **kwargs):
        ctx = super().get_context(request, **kwargs)
        ctx['form'] = self.get_form(request.POST)
        return ctx

    def filter_user_submission_payload(self, request, payload):
        return {'value': float(payload.get('value') or 0)}


class NumericProgress(QuestionProgress):
    """
    Progress class for numeric questions.
    """


class NumericSubmission(QuestionSubmission):
    """
    Submission class for numeric questions.
    """

    value = models.FloatField()


class NumericFeedback(QuestionFeedback):
    """
    Numeric feedback: autograde tests if value is within the requested interval.
    """

    def get_autograde_value(self):
        question = self.question
        submission = self.submission

        value = submission.value
        correct = question.correct_answer
        tol = question.tolerance

        return 100 if abs(value - correct) <= tol else 0, {}
