from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FreshInstallConfig(AppConfig):
    name = 'codeschool.extra.fresh_install'
    verbose_name = _('Fills initial db with sample data.')
