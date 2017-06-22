from django.utils.translation import ugettext_lazy as _
from codeschool.fixes.wagtailadmin import WagtailAdmin
from codeschool.models import Page
from codeschool import panels
from . import models


class AttendancePageAdmin(WagtailAdmin):

    class Meta:
        model = models.AttendancePage
        abstract = True

    subpage_types = []

    content_panels = \
        Page.content_panels + [
            panels.InlinePanel('attendance_sheet_single_list',
                               max_num=1, min_num=1),
        ]


models.AttendanceSheet.panels = [
    panels.FieldPanel('max_attempts'),
    panels.FieldPanel('expiration_minutes'),
    panels.FieldPanel('max_string_distance'),
]
