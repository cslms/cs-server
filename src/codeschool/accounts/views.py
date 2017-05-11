from django import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from userena import views
from userena.forms import AuthenticationForm

from codeschool.models import User
from . import bricks
from .forms import SignupForm, SignupOptionalForm


class LoginView(TemplateView):
    """
    View for the default login page.
    """

    template_name = 'auth/login.jinja2'

    def get_context_data(self, **kwargs):

        return super().get_context_data(
            signin=AuthenticationForm(),
            signup=SignupForm(),
            signup_opt=SignupOptionalForm(),
            **kwargs
        )

    def post(self, request):
        if request.POST['action'] == 'signup':
            return self.post_signup(request)
        else:
            return self.post_signin(request)

    def post_signin(self, request):
        return views.signin(
            request,
            template_name='auth/login.jinja2',
            extra_context=self.get_context_data(action='signin')
        )

    def post_signup(self, request):
        context = self.get_context_data(action='signup')
        form = SignupForm(request.POST)
        opt_form = SignupOptionalForm(request.POST)

        # Render forms if they are invalid
        if not (opt_form.is_valid() and form.is_valid()):
            context['signup'] = form
            context['signup_opt'] = opt_form
            return super().render_to_response(context)

        # Validate and proceed
        context['signup_opt'] = opt_form
        response = views.signup(
            request,
            signup_form=SignupForm,
            template_name=self.template_name,
            extra_context=context,
            success_url='/',
        )

        # It redirects on success: we intercept and add extra
        # information
        if isinstance(response, http.HttpResponseRedirect):
            # Fill extra info in signup form
            aux = form.cleaned_data
            user = User.objects.get(username=aux['username'])
            user.first_name = aux['first_name']
            user.last_name = aux['last_name']

            # Fill extra profile info
            opt_form = SignupOptionalForm(request.POST)
            opt_form.is_valid()
            aux = opt_form.cleaned_data
            user.profile.about_me = aux['about_me']
            user.profile.gender = aux['gender']
            user.profile.date_of_birth = aux['date_of_birth']

            # Save modifications and go
            user.save()
            user.profile.save()
            return redirect('index')
        return response


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
