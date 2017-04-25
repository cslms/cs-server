from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from codeschool import panels
from codeschool.fixes.wagtailadmin import WagtailAdmin
from .models import Classroom, ClassroomList


class ClassroomAdmin(WagtailAdmin):
    """
    Wagtail admin options for the Classroom model.
    """

    class Meta:
        model = Classroom

    subpage_types = None
    parent_page_types = [ClassroomList]
    content_panels = \
        WagtailAdmin.content_panels + [
            panels.MultiFieldPanel([
                panels.FieldPanel('short_description'),
                panels.FieldPanel('description'),
                panels.FieldPanel('weekly_lessons'),
                panels.FieldPanel('template'),
            ], heading=_('Basic options')),

            panels.MultiFieldPanel([
                panels.FieldPanel('teacher'),
                # panels.FieldPanel('staff'),
            ], heading=_('Users and staff'),
                classname='collapsible collapsed'),

            panels.MultiFieldPanel([
                panels.FieldPanel('accept_subscriptions'),
                panels.FieldPanel('subscription_passphrase'),
                panels.FieldPanel('is_public'),
            ], heading=_('Subscriptions'),
                classname='collapsible collapsed'),
        ]


# Parent pages and subpages
ClassroomList.parent_page_types = []
ClassroomList.subpage_types = [Classroom]

# Django register
admin.site.register(Classroom)
admin.site.register(ClassroomList)
