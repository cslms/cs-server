import logging

from django.contrib.auth import login
from django.shortcuts import render

from codeschool import models
from codeschool.core.config import config_options, global_data_store
from codeschool.core.config.views import index_view
from codeschool.core.users.models import Profile
from codeschool.extra.fresh_install.data_providers import fill_data
from codeschool.extra.fresh_install.factories import maurice_moss_profile
from .forms import ConfigForm, NewUserForm, \
    SysProfileForm, PasswordForm

log = logging.getLogger('codeschool.fresh_install')


def configure_server_view(request):
    """
    Exhibit a form that performs basic server configuration.
    """

    has_superuser = site_has_superuser()
    context = {
        'config': config_options,
        'user': request.user,
        'disable_footer_data': True,
        'disable_nav': False,
        'create_superuser': not has_superuser,
        'options_form': ConfigForm(),
        'superuser_form': NewUserForm(),
        'sys_profile_form': SysProfileForm(),
        'password_form': PasswordForm(request.POST),
    }

    if not request.user.is_superuser and has_superuser:
        return render(request, 'fresh_install/forbidden.jinja2', {})

    if request.method == 'POST':
        return configure_server_view_post(request, context)

    return render(request, 'fresh_install/config.jinja2', context)


def configure_server_view_post(request, context):
    has_superuser = site_has_superuser()
    options_form = ConfigForm(request.POST)
    superuser_form = NewUserForm(request.POST)
    sys_profile_form = SysProfileForm(request.POST)
    password_form = PasswordForm(request.POST)
    forms = [options_form, sys_profile_form]

    if not has_superuser:
        forms.extend([superuser_form, password_form])

    if all(form.is_valid() for form in forms):
        # Create user
        if not has_superuser:
            user = create_superuser_from_forms(
                superuser_form,
                password_form
            )
            django_backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=django_backend)
        else:
            user = request.user
        global_data_store['admin-user-id'] = user.id

        # Populate the database
        fill_data(sys_profile_form.cleaned_data, user)

        # Save global settings
        data = options_form.cleaned_data
        config_options['address'] = data['address']
        config_options['initial-page'] = '/api/'
        return index_view(request)


def site_has_superuser():
    return (
        models.get_user_model()
        .objects
        .filter(is_superuser=True)
        .count() > 0
    )


def create_superuser_from_forms(superuser_form, password_form) -> models.User:
    user = superuser_form.save(commit=False)
    password = password_form.cleaned_data['password']
    password = password or 'admin'
    user.set_password(password)
    user.is_superuser = True
    user.is_active = True
    user.is_staff = True
    user.save()
    profile, _ = Profile.objects.get_or_create(user=user)

    # Easter egg-ish ;-)
    if user.name == 'Maurice Moss':
        maurice_moss_profile(profile)

    return user
