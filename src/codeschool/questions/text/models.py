from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext as __

from codeschool import models
from codeschool import panels
from codeschool.questions.models import Question, QuestionFeedback, \
    QuestionSubmission, QuestionProgress
from unidecode import unidecode

class TextQuestion(Question):
    """
    A very simple question with a simple Text answer.
    """
    class Meta:
        verbose_name = _('Text question')
        verbose_name_plural = _('Text questions')

    correct_answer = models.CharField(
        _('Correct answer'),
        help_text=_(
            'The expected Text answer for question.'
        ),
        max_length=100,
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
        class TextForm(forms.Form):
            value = forms.CharField(
                label=self.label, required=True, max_length=250)

        return TextForm

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(*args, **kwargs)

    # Serving Pages
    template = 'questions/text/detail.jinja2'

    def get_context(self, request, **kwargs):
        ctx = super().get_context(request, **kwargs)
        ctx['form'] = self.get_form(request.POST)
        return ctx

    def get_submission_kwargs(self, request, kwargs):
        return {'value': str(kwargs.get('value', None) or 0)}

    # Wagtail admin
    content_panels = Question.content_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('correct_answer'),
            panels.FieldPanel('label'),
            panels.FieldPanel('help_text'),
        ], heading=_('Text value'))
    ]
    content_panels.append(content_panels.pop(-2))


class TextProgress(QuestionProgress):
    pass


class TextSubmission(QuestionSubmission):
    value = models.CharField(max_length=100)

    def compute_hash(self):
        return str(hash(self.value))


class TextFeedback(QuestionFeedback):
    """
    Text feedback: autograde simply tests if value is within the requested
    interval.
    """

    def autograde(self):
        value = self.submission.value
        correct = self.question.correct_answer

        correct = unidecode(correct).lower()
        value = unidecode(value).lower()

        if value == correct:
            self.given_grade_pc = 100
        else:
            self.given_grade_pc = 0
