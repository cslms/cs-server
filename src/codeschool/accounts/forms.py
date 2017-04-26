from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from userena import forms as userena_forms

from codeschool.accounts import models
from codeschool.models import Page


class SignupForm(userena_forms.SignupForm):
    """
    We create a new SignupForm since we want to have required first and last
    names.
    """
    _field_ordering = ['first_name', 'last_name']
    _field_ordering.extend(userena_forms.SignupForm.base_fields)

    first_name = forms.CharField(
        label=_('First name'),
        max_length=100,
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=100,
    )

# Reorder fields
SignupForm.base_fields = OrderedDict(
    (k, SignupForm.base_fields[k]) for k in SignupForm._field_ordering
)


class SignupOptionalForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = ['gender', 'date_of_birth', 'about_me']


class EditProfileForm(userena_forms.EditProfileForm):

    class Meta:
        page_fields = [field.name for field in Page._meta.concrete_fields]
        model = models.Profile
        exclude = ['user', 'content_color', 'is_teacher']
