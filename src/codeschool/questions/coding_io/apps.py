from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CodingIoQuestionConfig(AppConfig):
    name = 'codeschool.questions.coding_io'
    label = 'question_codingio'
    verbose_name = _('IO-based programming questions')
