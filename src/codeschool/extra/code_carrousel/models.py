from django.utils.translation import ugettext_lazy as _
from codeschool import models
from codeschool import panels
from codeschool import blocks
from . import Activity


class CodeCarouselItem(models.Orderable):
    """
    A simple state of the code in a SyncCodeActivity.
    """

    activity = models.ParentalKey(
        'cs_core.CodeCarouselActivity',
        related_name='items'
    )
    text = models.TextField()
    timestamp = models.DateTimeField(
        auto_now=True
    )

    # Wagtail admin
    panels = [
        panels.FieldPanel('text', widget=blocks.AceWidget()),
    ]


class CodeCarouselActivity(Activity):
    """
    In this activity, the students follow a piece of code that someone
    edit and is automatically updated in all of student machines. It keeps
    track of all modifications that were saved by the teacher.
    """

    class Meta:
        verbose_name = _('synchronized code activity')
        verbose_name_plural = _('synchronized code activities')

    default_material_icon = 'code'
    language = models.ForeignKey(
        'ProgrammingLanguage',
        on_delete=models.PROTECT,
        related_name='sync_code_activities',
        help_text=_('Chooses the programming language for the activity'),
    )

    @property
    def last(self):
        try:
            return self.items.order_by('timestamp').last()
        except CodeCarouselItem.DoesNotExist:
            return None

    @property
    def first(self):
        try:
            return self.items.order_by('timestamp').first()
        except CodeCarouselItem.DoesNotExist:
            return None

    # Wagtail admin
    content_panels = models.CodeschoolPage.content_panels + [
        panels.MultiFieldPanel([
            panels.RichTextFieldPanel('short_description'),
            panels.FieldPanel('language'),
        ], heading=_('Options')),
        panels.InlinePanel('items', label='Items'),
    ]
