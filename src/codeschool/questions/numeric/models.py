from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext as __

from codeschool import models
from codeschool import panels
from codeschool.questions.models import Question, QuestionFeedback, \
    QuestionSubmission, QuestionProgress


class NumericQuestion(Question):
    """
    A very simple question with a simple numeric answer.
    """
    class Meta:
        verbose_name = _('Numeric question')
        verbose_name_plural = _('Numeric questions')

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

    instant_autograde = True

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

    def get_submission_kwargs(self, request, kwargs):
        return {'value': float(kwargs.get('value', None) or 0)}

    # Wagtail admin
    content_panels = Question.content_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('correct_answer'),
            panels.FieldPanel('tolerance'),
            panels.FieldPanel('label'),
            panels.FieldPanel('help_text'),
        ], heading=_('Numeric value'))
    ]
    content_panels.append(content_panels.pop(-2))


class NumericProgress(QuestionProgress):
    pass


class NumericSubmission(QuestionSubmission):
    value = models.FloatField()

    def compute_hash(self):
        return str(hash(self.value))


class NumericFeedback(QuestionFeedback):
    """
    Numeric feedback: autograde simply tests if value is within the requested
    interval.
    """

    def autograde(self):
        value = self.submission.value
        correct = self.question.correct_answer
        tol = self.question.tolerance

        if abs(value - correct) <= tol:
            self.given_grade_pc = 100
        else:
            self.given_grade_pc = 0

NumericQuestion.submission_class = NumericSubmission
