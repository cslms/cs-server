from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.fixes.wagtailadmin import WagtailAdmin
from codeschool.mixins import ShortDescriptionPageMixin
from . import models


class QuestionAdmin(WagtailAdmin):

    class Meta:
        model = models.Question
        abstract = True

    subpage_types = []

    content_panels = \
        ShortDescriptionPageMixin.content_panels[:-1] + [
            panels.MultiFieldPanel([
                panels.FieldPanel('import_file'),
                panels.FieldPanel('short_description'),
            ], heading=_('Options')),
            panels.StreamFieldPanel('body'),
            panels.MultiFieldPanel([
                panels.FieldPanel('author_name'),
                panels.FieldPanel('comments'),
            ], heading=_('Optional information'),
                classname='collapsible collapsed'),
        ]
