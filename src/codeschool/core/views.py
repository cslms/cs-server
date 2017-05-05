import logging

import model_reference
from django.contrib.auth import login
from django.shortcuts import render, redirect

from codeschool import models
from codeschool import settings
from codeschool.core import config_options, global_data_store
from codeschool.accounts.models import Profile
from codeschool.core.debug_info import DebugInfo
from codeschool.core.forms import ConfigForm, NewUserForm, SysProfileForm, \
    PasswordForm

log = logging.getLogger('codeschool.core')


def debug_page_view(request):
    """
    Shows debug information about codeschool.
    """

    info = DebugInfo(user=request.user)
    return render(request, 'core/debug.jinja2', dict(info))


def index_view(request):
    """
    Simple index view. Redirect to login or to user profile page.
    """

    initial = config_options.get('initial-page', None)
    if initial is None:
        return configure_server_view(request)

    if request.user.is_anonymous():
        return redirect('auth:login')

    return redirect(config_options['initial-page'])


def configure_server_view(request):
    """
    Exhibit a form that performs basic server configuration.
    """

    has_superuser = site_has_superuser()
    if not request.user.is_superuser and has_superuser:
        return render(request, 'core/forbidden-server-config.jinja2', {})

    context = {
        'config': config_options,
        'user': request.user,
        'disable_footer_data': True,
        'disable_nav': False,
        'create_superuser': not has_superuser,
    }

    if request.method == 'POST':
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
                user = create_superuser_from_forms(superuser_form,
                                                   password_form)
                django_backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=django_backend)
            else:
                user = request.user
            global_data_store['admin-user-id'] = user.id

            # Populate the database
            data = sys_profile_form.cleaned_data
            if data.get('joe_user', False):
                fill_joe_user()
            if data.get('basic_activities', False):
                fill_basic_activities()
            if data.get('example_questions', False):
                fill_example_questions(user)
            if data.get('example_courses', False):
                fill_example_courses()
            if data.get('populate_courses', False):
                fill_courses_with_users()
            if data.get('exapmle_submissions', False):
                fill_example_submissions()

            # Ensure references to important pages were created
            model_reference.load('main-question-list')
            if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
                model_reference.load('course-list')

            # Save global settings
            data = options_form.cleaned_data
            config_options['address'] = data['address']
            config_options['initial-page'] = data['initial_page']
            return index_view(request)
    else:
        options_form = ConfigForm()
        superuser_form = NewUserForm()
        sys_profile_form = SysProfileForm()
        password_form = PasswordForm(request.POST)

    context['options_form'] = options_form
    context['superuser_form'] = superuser_form
    context['sys_profile_form'] = sys_profile_form
    context['password_form'] = password_form

    return render(request, 'core/server-config.jinja2', context)


def site_has_superuser():
    """
    Return True if site has a superuser defined.
    """

    return models.User.objects.filter(is_superuser=True).count() > 0


def fill_maurice_moss_profile(profile: Profile):
    log.info('Moss is the sysadmin!')
    profile.date_or_birth = (1982, 1, 6)
    profile.gender = profile.GENDER_MALE
    profile.website = 'https://www.reynholm.co.uk/~moss/'
    profile.about_me = (
        "Hi everyone and welcome to my web page. "
        "My name is Maurice Moss, my friends call me Moss. "
        "I'm a single I.T. guy from London, I'm in my 30's, "
        "I live with my mother, and I work for Reynholm Industries."
    )
    profile.phone = '+44 20 7946 3108 x3171'  # taken from facebook page
    profile.save()


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
    if user.first_name == 'Maurice' and user.last_name == 'Moss':
        fill_maurice_moss_profile(profile)

    return user


def fill_joe_user():
    from codeschool.accounts.factories import make_joe_user

    joe = make_joe_user()
    global_data_store['joe-user-id'] = joe.id


def fill_basic_activities():
    from codeschool.lms.activities.factories import make_basic_activities

    if 'main-question-list' not in global_data_store:
        global_data_store['main-question-list'] = 'basic'
        make_basic_activities()


def fill_example_questions(user):
    from codeschool.core.factories import make_example_questions

    if not global_data_store.get('example-questions', False):
        global_data_store['example-questions'] = True
        activities = model_reference.load('main-question-list')
        questions = make_example_questions(activities)
        for i in range(1, min(2, len(questions))):
            questions[i].owner = user
            questions[i].save()


def fill_example_courses():
    from codeschool.lms.courses.factories import make_example_courses

    if not global_data_store.get('example-courses', False):
        global_data_store['example-courses'] = True
        cs101, *other_courses = make_example_courses()
        cs101.teacher = models.User.objects.get(
            id=global_data_store['admin-user-id'])
        cs101.save()


def fill_courses_with_users():
    from codeschool.lms.courses.models import Course
    from codeschool.accounts.factories import make_teachers, make_joe_user, \
        make_mr_robot

    if not global_data_store.get('courses-populated', False):
        user = models.User.objects.get(id=global_data_store['admin-user-id'])
        global_data_store['courses-populated'] = True
        teachers = [user]
        teachers.extend(make_teachers())
        common = [make_mr_robot(), make_joe_user()]

        for teacher, course in zip(teachers, Course.objects.all()):
            from codeschool.accounts.factories import make_students
            for student in list(make_students(3)) + common:
                course.enroll_student(student)
            course.teacher = teacher
            course.save()


def fill_example_submissions():
    if not global_data_store.get('example-submissions'):
        global_data_store['example-submissions'] = True

        # TODO: implement this
        # make_example_submissions()
