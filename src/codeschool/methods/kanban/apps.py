from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KanbanConfig(AppConfig):
    name = 'codeschool.methods.kanban'
    verbose_name = _('Kanban')
