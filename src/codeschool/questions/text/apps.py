from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TextQuestionConfig(AppConfig):
    name = 'codeschool.questions.text'
    label = 'question_text'
    verbose_name = _('Text-based questions')
