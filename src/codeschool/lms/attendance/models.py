import collections
import datetime
from types import FunctionType

import bricks.rpc
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from lazyutils import delegate_to

from codeschool import models
from codeschool.types.rules import Rules
from codeschool.utils.phrases import phrase
from codeschool.utils.string import string_distance


class AttendanceSheet(models.Model):
    """
    Controls student attendance by generating a new public pass-phrase under
    teacher request. Students confirm attendance by typing the secret phrase
    within a small interval after the teacher starts checking the attendance.
    """

    max_attempts = models.SmallIntegerField(
        _('Maximum number of attempts'),
        default=3,
        help_text=_(
            'How many times a student can attempt to prove attendance. A '
            'maximum is necessary to avoid a brute force attack.'
        ),
    )
    expiration_minutes = models.SmallIntegerField(
        _('Expiration time'),
        default=5,
        help_text=_(
            'Time (in minutes) before attendance session expires.'
        )
    )
    owner = models.ForeignKey(models.User)
    last_event = models.ForeignKey('Event', blank=True, null=True)
    max_string_distance = models.SmallIntegerField(
        _('Fuzzyness'),
        default=1,
        help_text=_(
            'Maximum number of wrong characters that is considered acceptable '
            'when comparing the expected passphrase with the one given by the'
            'student.'
        ),
    )
    max_number_of_absence = models.IntegerField(blank=True, null=True)

    # Properties
    expiration_interval = property(
        lambda self: datetime.timedelta(minutes=self.expiration_minutes))
    attendance_checks = property(
        lambda self: AttendanceCheck.objects.filter(event__sheet=self)
    )

    def __str__(self):
        try:
            return self.attendancepage_set.first().title
        except models.ObjectDoesNotExist:
            user = self.owner.get_full_name() or self.owner.username
            return _('Attendance sheet (%s)' % user)

    def new_event(self, commit=True):
        """
        Create a new event in attendance sheet.
        """

        current_time = now()
        event = Event(
            passphrase=phrase(),
            date=current_time.date(),
            created=current_time,
            expires=current_time + self.expiration_interval,
            sheet=self,
        )
        self.last_event = event
        if commit:
            event.save()
            self.save(update_fields=['last_event'])
        return event

    def current_passphrase(self):
        """
        Return the current passphrase.
        """
        return self.current_event().passphrase

    def current_event(self):
        """
        Return the last event created for today.

        If no event is found, create a new one.
        """

        if self.last_event and self.last_event.date == now().date():
            return self.last_event
        else:
            return self.new_event()

    def number_of_absences(self, user):
        """
        Return the total number of absence for user.
        """

        return self.attendance_checks.filter(user=user,
                                             has_attended=False).count()

    def absence_table(self, users=None, method='fraction'):
        """
        Return a mapping between users and their respective absence rate. 

        Args:
            users:
                A queryset of users.
            method:
                One of 'fraction' (default), 'number', 'attendance' or 
                'attendance-fraction'
        """

        try:
            get_value_from_absence = {
                'fraction': lambda x: x / num_events,
                'number': lambda x: x,
                'attendance': lambda x: num_events - x,
                'attendance-fraction': lambda x: (num_events - x) / num_events
            }[method]
        except KeyError:
            raise ValueError('invalid method: %r' % method)

        num_events = self.events.count()
        if users is None:
            users = models.User.objects.all()

        result = collections.OrderedDict()
        for user in users:
            absence = self.user_absence(user)
            result[user] = get_value_from_absence(absence)
        return result

    def user_attempts(self, user):
        """
        Return the number of user attempts in the last attendance event.
        """

        if self.last_event is None:
            return 0

        qs = self.attendance_checks.filter(user=user, event=self.last_event)
        return qs.count()

    def minutes_left(self, raises=True):
        """
        Return how many minutes left for expiration.
        """

        if self.last_event:
            time = now()
            if self.last_event.expires < time:
                return 0.0
            else:
                dt = self.last_event.expires - time
                return dt.total_seconds() / 60.
        if raises:
            raise ValueError('last event is not defined')
        else:
            return None

    def is_expired(self):
        """
        Return True if last_event has already expired.
        """

        if not self.last_event:
            return False
        return self.last_event.expires < now()

    def is_valid(self, passphrase):
        """
        Check if passphrase is valid.
        """
        if self.is_expired():
            return False
        distance = string_distance(passphrase, self.current_passphrase())
        return distance <= self.max_string_distance


class Event(models.Model):
    """
    Represents an event that we want to confirm attendance.
    """

    sheet = models.ForeignKey(AttendanceSheet, related_name='events')
    date = models.DateField()
    created = models.DateTimeField()
    expires = models.DateTimeField()
    passphrase = models.CharField(
        _('Passphrase'),
        max_length=200,
        help_text=_(
            'The passphrase is case-insensitive. We tolerate small typing '
            'errors.'
        ),
    )

    def update(self, commit=True):
        """
        Regenerate passphrase and increases expiration time.
        """

        new = self.passphrase
        while new == self.passphrase:
            new = phrase()
        self.passphrase = new
        self.expires += self.sheet.expiration_interval
        if commit:
            self.save()


class AttendanceCheck(models.Model):
    """
    Confirms attendance by an user.
    """

    user = models.ForeignKey(models.User)
    event = models.ForeignKey(Event)
    has_attended = models.BooleanField(default=bool)
    attempts = models.SmallIntegerField(default=int)

    def update(self, phrase):
        """
        Update check with the given passphrase.
        """

        sheet = self.event.sheet
        if self.attempts > sheet.max_attempts:
            return
        if string_distance(phrase,
                           self.event.passphrase) <= sheet.max_string_distance:
            self.has_attended = True
        self.attempts += 1
        self.save()


class AttendancePage(models.DecoupledAdminPage, models.RoutableViewsPage):
    """
    A Page object that exhibit an attendance sheet.
    """

    rules = Rules()

    @property
    def attendance_sheet(self):
        try:
            return self._attendance_sheet
        except AttributeError:
            pass

        try:
            self._attendance_sheet = self.attendance_sheet_single_list.first()
            return self._attendance_sheet
        except models.ObjectDoesNotExist:
            return None

    @attendance_sheet.setter
    def attendance_sheet(self, value):
        sheet = AttendanceSheetChild(owner=self.owner)
        self.attendance_sheet_single_list = [sheet]
        self._attendance_sheet = sheet

    expiration_interval = delegate_to('attendance_sheet')
    last_event = delegate_to('attendance_sheet')
    max_attempts = delegate_to('attendance_sheet')
    max_string_distance = delegate_to('attendance_sheet')

    @classmethod
    def _update_model(cls):
        for k, v in vars(AttendanceSheet).items():
            if k.startswith('_') or not isinstance(v, FunctionType):
                continue
            setattr(cls, k, delegate_to('attendance_sheet'))

    def clean(self):
        if self.attendance_sheet is None:
            self.attendance_sheet = AttendanceSheet(owner=self.owner)
        self.attendance_sheet.owner = self.attendance_sheet.owner or self.owner
        self.title = str(self.title or _('Attendance sheet'))
        super().clean()

    def get_context(self, request, *args, **kwargs):
        from . import forms

        is_teacher = self.rules.has_perm(request.user,
                                         'attendance.see_passphrase')

        ctx = super().get_context(request)
        ctx['is_teacher'] = is_teacher
        ctx['attendance_sheet'] = self.attendance_sheet
        ctx['form'] = forms.PassphraseForm() if not is_teacher else None
        ctx['passphrase'] = self.current_passphrase() if is_teacher else None
        ctx['is_expired'] = self.is_expired()
        return ctx

    @bricks.rpc.route(r'^check.api/$')
    def check_presence(self, client, passphrase, **kwargs):
        html = ('<div class="cs-attendance-dialog cs-attendance-dialog--%s">'
                '<h1>%s</h1>'
                '<p>%s</p>'
                '</div>')

        if self.is_valid(passphrase):
            html = html % ('success', _('Yay!'), _('Presence confirmed!'))
        else:
            html = html % (
                'failure', _('Oh oh!'),
                _('Could not validate this passphrase :-('))
        client.dialog(html=html)


class AttendanceSheetChild(AttendanceSheet):
    """
    A attendance sheet associated with a page.

    This hack is required since wagtail cannot edit sub-fields inplace. We
    should make a patch and fix this someday. Create a InlineObjectPanel().
    """

    page = models.ParentalKey(AttendancePage,
                              related_name='attendance_sheet_single_list')


AttendancePage._update_model()
