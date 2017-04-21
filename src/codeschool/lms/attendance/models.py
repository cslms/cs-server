import collections

import datetime
from random import choice

import editdistance as editdistance
from django.template.loader import render_to_string
from django.utils.timezone import now

from codeschool import models


class AttendanceSheet(models.Model):
    """
    Controls student attendance by generating a new public passphrase under 
    teacher request. Students confirm attendance by typing the secret phrase
    in a small interval. 
    """

    max_attempts = models.SmallIntegerField(default=3)
    expiration_minutes = models.SmallIntegerField(default=5)
    owner = models.ForeignKey(models.User)
    last_event = models.ForeignKey('Event', blank=True, null=True)
    max_string_distance = models.SmallIntegerField(default=0)
    max_number_of_absence = models.IntegerField(blank=True, null=True)

    @property
    def expiration_interval(self):
        return datetime.timedelta(minutes=self.expiration_minutes)

    @property
    def attendance_checks(self):
        return AttendanceCheck.objects.filter(event__sheet=self)

    def new_event(self):
        """
        Create a new event in attendance sheet.
        """

        current_time = now()
        new = self.events.create(
            passphrase=new_random_passphrase(),
            date=current_time.date(),
            created=current_time,
            expires=current_time + self.expiration_interval
        )
        self.last_event = new
        self.save(update_fields=['last_event'])
        return new

    def get_today_event(self):
        """
        Return the last event created for today
        """

        if self.last_event.date() == now().date():
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

    def render_dialog(self, request):
        """
        Renders attendance dialog based on request.
        """

        context = {
            'passphrase': self.passphrase,
            'is_expired': self.is_expired(),
            'minutes_left': self.minutes_left(raises=False)
        }
        user = request.user
        if user == self.owner:
            template = 'attendance/edit.jinja2'
        else:
            template = 'attendance/view.jinja2'
            context['attempts'] = self.user_attempts(user)
        return render_to_string(template, request=request, context=context)

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
                return dt.minutes
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


class Event(models.Model):
    """
    Represents an event that we want to confirm attendance.
    """

    sheet = models.ForeignKey(AttendanceSheet, related_name='events')
    date = models.DateField()
    created = models.DateTimeField()
    expires = models.DateTimeField()
    passphrase = models.CharField(max_length=100)

    def update(self):
        """
        Regenerate passphrase and increases expiration time.
        """

        self.passphrase = new_random_passphrase()
        self.expires += self.sheet.expiration_interval
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


def string_distance(str1, str2):
    str1 = str1.casefold()
    str2 = str2.casefold()
    if str1 == str2:
        return 0
    else:
        return editdistance.eval(str1, str2)


def new_random_passphrase():
    return '%s %s' % (choice(PERSON), choice(ADJECTIVE))


PERSON = [
    # Physicists
    'Einstein', 'Newton', 'Dirac', 'Bohr', 'Rutherford', 'Heisenberg',
    'Curie', 'Langevin', 'Boltzmann',

    # Mathematicians
    'Pythagoras', 'Peano', 'Hilbert', 'Gauss', 'Galois',

    # Computer science
    'Knuth', 'Turing',
]

ADJECTIVE = [
    'mal-humorado', 'pedante', 'esperto', 'manhoso',
]
