from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.utils.text import slugify
from wagtail.wagtailcore import blocks
from codeschool import models
from codeschool import panels
from codeschool.utils import delegate_to


class Calendar(models.Page):
    """
    A page that gathers a list of lessons in the course.
    """

    @property
    def course(self):
        return self.get_parent()

    weekly_lessons = delegate_to('course')

    def __init__(self, *args, **kwargs):
        if not args:
            kwargs.setdefault('title', __('Calendar'))
            kwargs.setdefault('slug', 'calendar')
        super().__init__(*args, **kwargs)

    def add_lesson(self, lesson, copy=True):
        """
        Register a new lesson in the course.

        If `copy=True` (default), register a copy.
        """

        if copy:
            lesson = lesson.copy()
        lesson.move(self)
        lesson.save()

    def new_lesson(self, *args, **kwargs):
        """
        Create a new lesson instance by calling the Lesson constructor with the
        given arguments and add it to the course.
        """

        kwargs['parent_node'] = self
        return LessonInfo.objects.create(*args, **kwargs)

    # Wagtail admin
    parent_page_types = ['courses.Course']
    subpage_types = ['courses.Lesson']
    content_panels = models.Page.content_panels + [
        panels.InlinePanel(
            'info',
            label=_('Lessons'),
            help_text=_('List of lessons for this course.'),
        ),
    ]


class Lesson(models.Page):
    """
    A single lesson in an ordered list.
    """

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    body = models.StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ],
        blank=True,
        null=True
    )

    date = delegate_to('lesson')
    calendar = property(lambda x: x.get_parent())

    def save(self, *args, **kwargs):
        lesson = getattr(self, '_created_for_lesson', None)
        if self.pk is None and lesson is None:
            calendar = lesson.calendar
            ordering = calendar.info.values_list('sort_order', flat=True)
            calendar.lessons.add(Lesson(
                title=self.title,
                page=self,
                sort_order=max(ordering) + 1,
            ))
            calendar.save()

    # Wagtail admin
    parent_page_types = ['courses.Calendar']
    subpage_types = []
    content_panels = models.Page.content_panels + [
        panels.StreamFieldPanel('body'),
    ]


class LessonInfo(models.Orderable):
    """
    Intermediate model between a LessonPage and a Calendar to make it
    orderable.
    """

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    calendar = models.ParentalKey(
        Calendar,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='info',
    )
    page = models.OneToOneField(
        Lesson,
        null=True, blank=True,
        related_name='info',
    )
    title = models.TextField(
        _('title'),
        help_text=_('A brief description for the lesson.'),
    )
    date = models.DateField(
        _('date'),
        null=True,
        blank=True,
        help_text=_('Date scheduled for this lesson.'),
    )

    def save(self, *args, **kwargs):
        if self.pk is None and self.page is None:
            self.page = lesson_page = Lesson(
                title=self.title,
                slug=slugify(self.title),
            )
            lesson_page._created_for_lesson = self
            self.calendar.add_child(instance=lesson_page)
        super().save(*args, **kwargs)

    panels = [
        panels.FieldPanel('title'),
        panels.FieldPanel('date'),
    ]
