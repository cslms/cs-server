from django.utils.translation import ugettext_lazy as _
from codeschool import models
from codeschool import blocks
from codeschool import panels
from . import Activity


class ContentActivity(Activity):
    """
    Content activities simply show a content to the students.
    """

    class Meta:
        verbose_name = _('content activity')
        verbose_name_plural = _('content activities')

    body = models.StreamField([
        #('paragraph', blocks.RichTextBlock()),
        #('page', blocks.PageChooserBlock()),
        #('file_list', blocks.ListBlock(blocks.DocumentChooserBlock())),
        #('code', blocks.CodeBlock()),
    ])

    # Wagtail admin
    content_panels = Activity.content_panels + [
        panels.StreamFieldPanel('body'),
    ]
