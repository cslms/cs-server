from collections import OrderedDict

import model_reference
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.utils.phrases import phrase

# User-facing strings
from bricks.helpers import hyperlink
from codeschool.lms.classrooms.managers import ClassroomManager

ACTIVITY_DESCRIPTION = _('Activities for the %(name)s course')


def random_subscription_passphase():
    return phrase().lower()


class Classroom(models.TimeStampedModel,
                models.DecoupledAdminPage,
                models.RoutableViewsPage):
    """
    One specific occurrence of a course for a given teacher in a given period.
    """

    discipline = models.ForeignKey('academic.Discipline',
                                   blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(models.User,
                                related_name='classrooms_as_teacher',
                                on_delete=models.PROTECT)
    students = models.ManyToManyField(
        models.User,
        related_name='classrooms_as_student',
        blank=True,
    )
    staff = models.ManyToManyField(
        models.User,
        related_name='classrooms_as_staff',
        blank=True,
    )
    weekly_lessons = models.BooleanField(
        _('weekly lessons'),
        default=False,
        help_text=_(
            'If true, the lesson spans a whole week. Otherwise, each lesson '
            'would correspond to a single day/time slot.'
        ),
    )
    accept_subscriptions = models.BooleanField(
        _('accept subscriptions'),
        default=True,
        help_text=_(
            'Set it to false to prevent new student subscriptions.'
        ),
    )
    is_public = models.BooleanField(
        _('is it public?'),
        default=True,
        help_text=_(
            'If true, all students will be able to see the contents of the '
            'course. Most activities will not be available to non-subscribed '
            'students.'
        ),
    )
    subscription_passphrase = models.CharField(
        _('subscription passphrase'),
        default=random_subscription_passphase,
        max_length=140,
        help_text=_(
            'A passphrase/word that students must enter to subscribe in the '
            'course. Leave empty if no passphrase should be necessary.'
        ),
        blank=True,
    )
    short_description = models.CharField(max_length=140)
    description = models.RichTextField()
    template = models.CharField(max_length=20, choices=[
        ('programming-beginner', _('A beginner programming course')),
        ('programming-intermediate', _('An intermediate programming course')),
        ('programming-marathon', _('A marathon-level programming course')),
    ], blank=True)

    objects = ClassroomManager()

    def save(self, *args, **kwargs):
        self.teacher = self.teacher or self.owner
        super().save(*args, **kwargs)

    def enroll_student(self, student):
        """
        Register a new student in the course.
        """

        if student == self.teacher:
            raise ValidationError(_('Teacher cannot enroll as student.'))
        elif student in self.staff.all():
            raise ValidationError(_('Staff member cannot enroll as student.'))
        self.students.add(student)
