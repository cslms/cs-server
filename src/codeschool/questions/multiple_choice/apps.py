from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MultipleChoiceQuestionConfig(AppConfig):
    name = 'codeschool.questions.multiple_choice'
    label = 'question_multiplechoice'
    verbose_name = _('Multiple-choice questions')