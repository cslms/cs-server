from django.utils.text import ugettext_lazy as _

from codeschool import panels
from codeschool.fixes.wagtailadmin import WagtailAdmin
from . import models


class QuestionAdmin(WagtailAdmin):
    class Meta:
        model = models.Question
        abstract = True

    subpage_types = []

    content_panels = [
        ...,

        # Main description
        panels.StreamFieldPanel('body'),

        # Options
        panels.MultiFieldPanel([
            panels.FieldPanel('author_name'),
            panels.FieldPanel('comments'),
        ], heading=_('Optional information'),
            classname='collapsible collapsed'),
    ]
