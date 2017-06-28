from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import mark_safe
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool import settings


def address_validator(value):
    if not value:
        raise ValidationError('invalid network address')


class NewUserForm(forms.ModelForm):
    """
    Create a new super user during initial configuration.
    """

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
    """
    Confirm password creation during initial configuration.
    """

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
        password = data.get('password')
        confirmation = data.get('password_confirmation')
        if password != confirmation:
            raise ValidationError(
                {'password_confirmation': _('Passwords must be equal!')})
        super().clean()


class ConfigForm(forms.Form):
    """
    Config server settings.
    """

    # Prepare valid initial page choices
    PAGE_DESCRIPTION = [_(
        '<span>Chooses which page is presented to users just after login.'
    ), '</span>\n <dl>\n', _(
        '<dt>Questions</dt> <dd>Show a global list of questions.</dd>\n'
    )]

    INITIAL_PAGE_OPTIONS = [('question-list', 'List of Questions')]
    if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
        INITIAL_PAGE_OPTIONS.append(('course-list', 'List of courses'))
        PAGE_DESCRIPTION += [_(
            '<dt>Courses</dt> <dd>Present a list of all courses related to the '
            'user.</dd>\n'
        )]
    if 'codeschool.social' in settings.INSTALLED_APPS:
        INITIAL_PAGE_OPTIONS.append(('social:timeline', 'Social network'))
        PAGE_DESCRIPTION += [_(
            '<dt>Social</dt> <dd>Start at user\'s news feed.</dd>\n'
            '</dl>'
        )]
    PAGE_DESCRIPTION += ['</dl>\n']
    PAGE_DESCRIPTION = ''.join(map(str, PAGE_DESCRIPTION))

    # Fields
    address = forms.CharField(
        max_length=200,
        label=_('Server address'),
        initial='codeschool.localhost',
        help_text=_(
            'Full network address for the Codeschool server.'
        ),
        validators=[address_validator],
    )
    initial_page = forms.ChoiceField(
        INITIAL_PAGE_OPTIONS,
        help_text=mark_safe(PAGE_DESCRIPTION)
    )


class SysProfileForm(forms.Form):
    """
    Configure initial database values.
    """

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
    if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
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
