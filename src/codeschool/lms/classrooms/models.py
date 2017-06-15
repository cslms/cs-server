from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.lms.classrooms.managers import ClassroomManager
from codeschool.utils.phrases import phrase

# User-facing strings
ACTIVITY_DESCRIPTION = _('Activities for the %(name)s course')


def random_subscription_passphase():
    return phrase().lower()


class Classroom(models.TimeStampedModel):
    """
    One specific occurrence of a course for a given teacher in a given period.
    """

    name = models.CharField(
        _('name'),
        max_length=64,
        help_text=_(
            'Classroom name'
        ),
    )
    slug = models.CodeschoolSlugField(
        primary_key=True,
    )
    discipline = models.ForeignKey(
        'academic.Discipline',
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    course = models.ForeignKey(
        'academic.Course',
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    teacher = models.ForeignKey(
        models.User,
        related_name='classrooms_as_teacher',
        on_delete=models.PROTECT
    )
    students = models.ManyToManyField(
        models.User,
        verbose_name=_('user'),
        related_name='classrooms_as_student',
        blank=True,
    )
    staff = models.ManyToManyField(
        models.User,
        verbose_name=_('staff'),
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
    short_description = models.CodeschoolShortDescriptionField()
    description = models.CodeschoolDescriptionField()

    objects = ClassroomManager()

    def register_student(self, user):
        """
        Register a new student in the course.
        """

        if user == self.teacher:
            raise ValidationError(_('Teacher cannot enroll as student.'))
        elif user in self.staff.all():
            raise ValidationError(_('Staff member cannot enroll as student.'))
        self.students.add(user)

    def register_staff(self, user):
        """
        Register a new user as staff.
        """

        if user == self.teacher:
            raise ValidationError(_('Teacher cannot enroll as staff.'))
        self.students.add(user)
