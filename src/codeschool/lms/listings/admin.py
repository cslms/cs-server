from codeschool import admin

from codeschool import panels
from .models import ActivityList, ActivitySection

admin.site.register(ActivityList)
admin.site.register(ActivitySection)


class ActivityListAdmin(admin.ShortDecriptionAdmin):

    class Meta:
        model = ActivityList

    # Wagtail admin
    subpage_types = ['ActivitySection']


class ActivitySectionAdmin(admin.ShortDecriptionAdmin):

    class Meta:
        model = ActivitySection

    # Wagtail admin
    subpage_types = ['ActivitySection']
    parent_page_types = [ActivityList]
    content_panels = admin.ShortDecriptionAdmin.content_panels + [
        panels.FieldPanel('material_icon')
    ]
