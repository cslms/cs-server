from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from codeschool import settings
from . import bricks
from .forms import LoginForm, UserForm, ProfileForm


def context():
    return dict(
        active_tab='login',
        login_form=LoginForm(),
        user_form=UserForm(),
        profile_form=ProfileForm(),
    )


def login_view_post(request):
    """
    Handles a POST request via login form.
    """

    ctx = context()
    ctx['login_form'] = form = LoginForm(request.POST)

    if form.is_valid():
        # Login
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(**form.cleaned_data)
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[-1])

        # Redirect
        redirect_url = request.GET.get('redirect', 'index')
        return redirect(redirect_url)
    else:
        return render(request, 'users/start.jinja2', ctx)


def register_view_post(request):
    """
    Handles a POST request via the signup form.
    """

    ctx = context()
    ctx['user_form'] = user_form = UserForm(request.POST)
    ctx['profile_form'] = profile_form = ProfileForm(request.POST)
    ctx['active_tab'] = 'register'

    if user_form.is_valid() and profile_form.is_valid():
        with transaction.atomic():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.id = user.id
            profile.user = user
            profile.save()

        user = authenticate(**user_form.cleaned_data)
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[-1])

        # Redirect
        redirect_url = request.GET.get('redirect', 'index')
        return redirect(redirect_url)
    else:
        return render(request, 'users/start.jinja2', ctx)


def start_view(request):
    """
    Handles GET request to the main /login/ url and redirect POSTs to the
    correct view function.
    """

    if request.method == 'POST':
        action = request.POST['action']
        if action == 'login':
            return login_view_post(request)
        elif action == 'register':
            return register_view_post(request)
        else:
            return http.HttpResponseBadRequest('invalid action')

    else:
        return render(request, 'users/start.jinja2', context())


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile
    name = profile.get_full_name_or_username()

    context = dict(
        content_title=_('Profile: {name}').format(name=name),
        content_body=bricks.profile(profile),
        navbar=bricks.navbar(user),
    )
    return render(request, 'base.jinja2', context)


def logout_view(request):
    ctx = {
        'post': request.method == 'POST',
    }

    if request.method == 'POST' and not request.user.is_anonymous():
        logout(request)
    return render(request, 'users/logout.jinja2', ctx)
