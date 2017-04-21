from django.utils.translation import ugettext_lazy as _

from codeschool import models, panels


class TimeSlot(models.Model):
    """
    Represents the weekly time slot that can be assigned to lessons for a
    given course.
    """

    class Meta:
        ordering = ('weekday', 'start')

    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
    WEEKDAY_CHOICES = [
        (MONDAY, _('Monday')),
        (TUESDAY, _('Tuesday')),
        (WEDNESDAY, _('Wednesday')),
        (THURSDAY, _('Thursday')),
        (FRIDAY, _('Friday')),
        (SATURDAY, _('Saturday')),
        (SUNDAY, _('Sunday'))
    ]
    course = models.ParentalKey(
        'Course',
        related_name='time_slots'
    )
    weekday = models.IntegerField(
        _('weekday'),
        choices=WEEKDAY_CHOICES,
        help_text=_('Day of the week in which this class takes place.')
    )
    start = models.TimeField(
        _('start'),
        blank=True,
        null=True,
        help_text=_('The time in which the class starts.'),
    )
    end = models.TimeField(
        _('ends'),
        blank=True,
        null=True,
        help_text=_('The time in which the class ends.'),
    )
    room = models.CharField(
        _('classroom'),
        max_length=100,
        blank=True,
        help_text=_('Name for the room in which this class takes place.'),
    )

    # Wagtail admin
    panels = [
        panels.FieldRowPanel([
            panels.FieldPanel('weekday', classname='col6'),
            panels.FieldPanel('room', classname='col6'),
        ]),
        panels.FieldRowPanel([
            panels.FieldPanel('start', classname='col6'),
            panels.FieldPanel('end', classname='col6'),
        ]),
    ]
