import uuid as uuid

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool import panels
from codeschool.questions.models import Question, QuestionFeedback, \
    QuestionSubmission, QuestionProgress


class MultipleChoiceQuestion(Question):
    """
    A very simple question with a simple numeric answer.
    """

    class Meta:
        verbose_name = _('Multiple choice question')
        verbose_name_plural = _('Multiple choice questions')

    instant_autograde = True
    __num_cleans = 0

    def clean(self):
        # FIXME: make validation works
        # Wagtail executes the clean method several times before validating
        # We need a way to validate only when all choices had been updated.
        # self.check_has_valid_choices()
        super().clean()

    def check_has_valid_choices(self):
        msg = _(
            'You must define at least one correct choice!\n'
            'The most valuable choice is worth {max_points} points.'
            'It should be exactly 100 points.')
        choices = self.choices.all()
        if not any(choice.value == 100 for choice in choices):
            max_points = max(choice.value for choice in choices)
            raise ValidationError([msg.format(max_points=max_points)])

    # Serving Pages
    template = 'questions/multiplechoice/detail.jinja2'

    def get_context(self, request, **kwargs):
        ctx = super().get_context(request, **kwargs)
        ctx['choices'] = self.choices.all()
        return ctx

    def filter_user_submission_payload(self, request, payload):
        choice_id = payload['choices']
        return {'choice_id': choice_id}

    # Wagtail admin
    content_panels = Question.content_panels + [
        panels.InlinePanel('choices', label=_('Choices')),
    ]
    content_panels.append(content_panels.pop(-2))


class Choice(models.Orderable):
    question = models.ParentalKey(MultipleChoiceQuestion,
                                  related_name='choices')
    text = models.RichTextField(_('Choice description'))
    uuid = models.UUIDField(default=uuid.uuid4)
    value = models.DecimalField(
        _('Value'), decimal_places=1, max_digits=4,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(100)],
        help_text=_(
            'Grade given for users that choose these option (value=0, for an '
            'incorrect choice and value=100 for a correct one).'
        ),
        default=0,
    )

    def __repr__(self):
        return 'Choice(value=%s, ...)' % self.value

    panels = [
        panels.FieldPanel('text'),
        panels.FieldPanel('value'),
    ]


class MultipleChoiceProgress(QuestionProgress):
    pass


class MultipleChoiceSubmission(QuestionSubmission):
    choice_id = models.CharField(max_length=32)


class MultipleChoiceFeedback(QuestionFeedback):
    """
    Numeric feedback: autograde simply tests if value is within the requested
    interval.
    """

    def update_autograde(self):
        choice_id = self.submission.choice_id
        choice = self.question.choices.get(uuid=choice_id)
        self.given_grade_pc = choice.value


MultipleChoiceQuestion.submission_class = MultipleChoiceSubmission
