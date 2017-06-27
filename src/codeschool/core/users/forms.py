from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models


class LoginForm(forms.Form):
    """
    Form used for user logins.
    """

    email = forms.EmailField(
        label=_('E-mail'),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
    )


class ProfileForm(forms.ModelForm):
    """
    Let users edit their profile and add sign-up data.
    """

    class Meta:
        model = models.Profile
        fields = 'gender', 'date_of_birth', 'website', 'phone', \
                 'about_me', 'visibility'


class UserForm(forms.ModelForm):
    """
    User creation form for sign-up.
    """

    class Meta:
        model = models.User
        fields = 'name', 'email', 'alias', 'school_id'
