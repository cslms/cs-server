from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FreeFormQuestionConfig(AppConfig):
    name = 'codeschool.questions.free_form'
    label = 'question_freeform'
    verbose_name = _('Free-form Questions')