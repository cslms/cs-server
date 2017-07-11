from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FormQuestionConfig(AppConfig):
    name = 'codeschool.questions.form'
    label = 'question_form'
    verbose_name = _('Form Questions')