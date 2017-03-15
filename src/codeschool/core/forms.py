from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import mark_safe
from django.utils.translation import ugettext_lazy as _

from codeschool import models


def address_validator(value):
    if not value:
        raise ValidationError('invalid network address')


class NewUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('initial', {
            'username': 'admin',
            'first_name': 'Maurice',
            'last_name': 'Moss',
            'email': 'moss.m@reynholm.co.uk',
        })
        super().__init__(*args, **kwargs)


class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=100, widget=forms.PasswordInput, required=False,
        help_text=_(
            'If you leave these fields blank, we assume the super-insecure '
            'password "admin".'
        )
    )
    password_confirmation = forms.CharField(max_length=100,
                                            widget=forms.PasswordInput,
                                            required=False)

    def clean(self):
        data = super().clean()
        password = data.get('password', None)
        confirmation = data.get('password_confirmation', None)
        if password != confirmation:
            raise ValidationError(
                {'password_confirmation': _('Passwords must be equal!')})
        super().clean()


class ConfigForm(forms.Form):
    address = forms.CharField(
        max_length=200,
        label=_('Server address'),
        initial='codeschool.localhost',
        help_text=_(
            'Full network address for the Codeschool server.'
        ),
        validators=[address_validator],
    )
    initial_page = forms.ChoiceField([
        ('course-list', 'List of courses'),
        ('activities-list', 'List of activities'),
        ('social:timeline', 'Social network'),
    ], help_text=mark_safe(_(
        '<span>Chooses which page is presented to users just after login.'
        '</span>\n'
        '<dl>\n'
        '<dt>Courses</dt> <dd>Present a list of all courses related to the '
        'user.</dd>\n'
        '<dt>Activities</dt> <dd>Show the global list of activities '
        'irrespective of any enrolled course.</dd>\n'
        '<dt>Social</dt> <dd>Start at user\'s news feed.</dd>\n'
        '</dl>'
    )))


class SysProfileForm(forms.Form):
    basic_activities = forms.BooleanField(
        initial=True,
        required=False,
        help_text=_(
            'Fill a list of basic activity sections covering many topics on '
            'an introductory level programming course.'
        )
    )
    example_questions = forms.BooleanField(
        initial=True,
        required=False,
        help_text=_(
            'Create a few example questions in the database. These are simple '
            'examples that help you get started with Codeshool.'
        )
    )
    example_courses = forms.BooleanField(
        initial=True,
        required=False,
        help_text=_(
            'Create a two programming courses pre-filled with data and '
            'student, teacher and staff profiles.'
        )
    )
    populate_courses = forms.BooleanField(
        initial=False,
        required=False,
        help_text=_(
            'Populate courses with random teachers and students.'
        )
    )
    joe_user = forms.BooleanField(
        label=_('Joe user'),
        required=False,
        help_text=_(
            'Creates an initial non-privileged user called "joe" (password: '
            'joe) so you can immediately test the site with regular accounts.'
        )
    )
    example_submissions = forms.BooleanField(
        required=False,
        help_text=_(
            'Create a few submissions to questions for both the admin user '
            'and regular users.'
        )
    )

    def clean(self):
        data = super().clean()
        populate = data.get('populate_courses', False)
        examples = data.get('example_courses', False)
        if populate and not examples:
            raise ValidationError({'populate_courses': _(
                'Must create courses first! Please confirm the "example '
                'courses" option.'
            )})
