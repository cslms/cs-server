from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ServicesConfig(AppConfig):
    name = 'codeschool.core.services'
    verbose_name = _('Interaction with external services')
