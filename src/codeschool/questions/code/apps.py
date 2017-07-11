from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CodeQuestionConfig(AppConfig):
    name = 'codeschool.questions.code'
    label = 'question_code'
    verbose_name = _('Code-based questions')
