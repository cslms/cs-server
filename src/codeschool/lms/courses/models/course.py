from collections import OrderedDict

import model_reference
from django import forms
from django.apps import apps
from django.db import transaction
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from lazyutils import lazy

from codeschool import models
from codeschool import panels
from codeschool.phrases import phrase

# User-facing strings
from bricks.helpers import hyperlink

ACTIVITY_DESCRIPTION = _('Activities for the %(name)s course')


def random_subscription_passphase():
    return phrase().lower()


class CourseManager(models.PageManager):
    def for_user(self, user):
        """
        Return a list of all courses related to user either as a student,
        teacher or staff member.
        """

        return (user.courses_as_teacher.all() \
                | user.courses_as_student.all() \
                | user.courses_as_staff.all()).distinct()

    def open_for_user(self, user):
        """
        List of courses that the user can subscribe.
        """

        user_courses = self.for_user(user)
        qs = self.filter(is_public=True, accept_subscriptions=True,
                         live=True)
        return qs.exclude(id__in=user_courses)


class PassPhraseForm(forms.Form):
    passphrase = forms.CharField(
        max_length=200,
        label=_('Pass-phrase'),
        help_text=_(
            'This is the secret registration pass-phrase the teacher provided.'
        )
    )


class Course(models.RoutablePageMixin, models.TimeStampedModel, models.Page):
    """
    One specific occurrence of a course for a given teacher in a given period.
    """

    discipline = models.ForeignKey('Discipline',
                                   blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(models.User,
                                related_name='courses_as_teacher',
                                on_delete=models.DO_NOTHING)
    students = models.ManyToManyField(
        models.User,
        related_name='courses_as_student',
        blank=True,
    )
    staff = models.ManyToManyField(
        models.User,
        related_name='courses_as_staff',
        blank=True,
    )
    weekly_lessons = models.BooleanField(
        _('weekly lessons'),
        default=False,
        help_text=_(
            'If true, the lesson spans a whole week. Othewise, each lesson '
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
    short_description = models.CharField(max_length=140, blank=True)
    description = models.RichTextField(blank=True)
    activities_template = models.CharField(max_length=20, choices=[
        ('programming-beginner', _('A beginner programming course')),
        ('programming-intermediate', _('An intermediate programming course')),
        ('programming-marathon', _('A marathon-level programming course')),
    ], blank=True)

    @lazy
    def academic_description(self):
        return getattr(self.discipline, 'description', '')

    @lazy
    def syllabus(self):
        return getattr(self.discipline, 'syllabus', '')

    objects = CourseManager()

    @property
    def calendar_page(self):
        content_type = models.ContentType.objects.get(
            app_label='cs_core',
            model='calendarpage'
        )
        return apps.get_model('cs_core', 'CalendarPage').objects.get(
            depth=self.depth + 1,
            path__startswith=self.path,
            content_type_id=content_type,
        )

    @property
    def activities_page(self):
        content_type = models.ContentType.objects.get(
            app_label='cs_questions',
            model='questionlist'
        )
        return apps.get_model('cs_questions', 'QuestionList').objects.get(
            depth=self.depth + 1,
            path__startswith=self.path,
            content_type_id=content_type,
        )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            created = self.id is None

            if not self.path:
                created = False
                root = model_reference.load('course-list')
                root.add_child(instance=self)
            else:
                super().save(*args, **kwargs)

            if created:
                self.create_calendar_page()
                self.create_activities_page()

    def create_calendar_page(self):
        """
        Creates a new calendar page if it does not exist.
        """

        model = apps.get_model('courses', 'calendar')
        calendar = model()
        self.add_child(instance=calendar)

    def create_activities_page(self):
        """
        Creates a new activities page if it does not exist.
        """

        model = apps.get_model('activities', 'activitylist')
        activities = model(
            title=_('Activities'),
            slug='activities',
            short_description=ACTIVITY_DESCRIPTION % {'name': self.title},
        )
        self.add_child(instance=activities)

    def enroll_student(self, student):
        """
        Register a new student in the course.
        """

        self.students.add(student)
        self.update_friendship_status(student)

    def is_registered(self, user):
        """
        Check if user is associated with the course in any way.
        """

        if self.teacher == user:
            return True
        elif user in self.students.all():
            return True
        elif user in self.staff.all():
            return True
        else:
            return False

    def update_friendship_status(self, student=None):
        """
        Recompute the friendship status for a single student by marking it as
        a colleague of all participants in the course.

        If no student is given, update the status of all enrolled students.
        """

        update = self._update_friendship_status
        if student is None:
            for student in self.students.all():
                update(student)
        else:
            update(student)

    def _update_friendship_status(self, student):
        for colleague in self.students.all():
            if colleague != student:
                FriendshipStatus.objects.get_or_create(
                    owner=student,
                    other=colleague,
                    status=FriendshipStatus.STATUS_COLLEAGUE)

    def get_user_role(self, user):
        """Return a string describing the most privileged role the user has
        as in the course. The possible values are:

        teacher:
            Owns the course and can do any kind of administrative tasks in
            the course.
        staff:
            Teacher assistants. May have some privileges granted by the teacher.
        student:
            Enrolled students.
        visitor:
            Have no relation to the course. If course is marked as public,
            visitors can access the course contents.
        """

        if user == self.teacher:
            return 'teacher'
        if user in self.staff.all():
            return 'staff'
        if user in self.students.all():
            return 'student'
        return 'visitor'

    def info_dict(self):
        """
        Return an ordered dictionary with relevant internationalized
        information about the course.
        """

        def yn(x):
            return _('Yes' if x else 'No')

        data = [
            ('Teacher', hyperlink(self.teacher)),
            ('Created', self.created),
            ('Accepting new subscriptions?', yn(self.accept_subscriptions)),
            ('Private?', yn(not self.is_public)),
        ]
        if self.academic_description:
            data.append(('Description', self.academic_description))
        if self.syllabus:
            data.append(('Description', self.academic_description))

        return OrderedDict([(_(k), v) for k, v in data])

    # Serving pages
    template = 'courses/detail.jinja2'

    def get_context(self, request, *args, **kwargs):
        return dict(
            super().get_context(request, *args, **kwargs),
            course=self,
        )

    def serve(self, request, *args, **kwargs):
        if self.is_registered(request.user):
            return super().serve(request, *args, **kwargs)
        return self.serve_registration(request, *args, **kwargs)

    def serve_registration(self, request, *args, **kwargs):
        context = self.get_context(request)
        if request.method == 'POST':
            form = PassPhraseForm(request.POST)
            if form.is_valid():
                self.enroll_student(request.user)
                return super().serve(request, *args, **kwargs)
        else:
            form = PassPhraseForm()

        context['form'] = form
        return render(request, 'courses/course-enroll.jinja2', context)

    # Wagtail admin
    parent_page_types = ['courses.CourseList']
    subpage_types = []
    content_panels = models.Page.content_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('short_description'),
            panels.FieldPanel('description'),
            panels.FieldPanel('teacher')
        ], heading=_('Options')),

        panels.InlinePanel(
            'time_slots',
            label=_('Time slots'),
            help_text=_('Define when the weekly classes take place.'),
        ),
    ]
    settings_panels = models.Page.settings_panels + [
        panels.MultiFieldPanel([
            panels.FieldPanel('weekly_lessons'),
        ], heading=_('Options')),
        panels.MultiFieldPanel([
            panels.FieldPanel('accept_subscriptions'),
            panels.FieldPanel('is_public'),
            panels.FieldPanel('subscription_passphrase'),
        ], heading=_('Subscription')),

    ]
