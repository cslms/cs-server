import model_reference
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .bricks import navbar_classroom, navbar_list
from .forms import EnrollForm
from .models import Classroom
from .rules import is_registered


@login_required
def list_of_classrooms(request):
    root = model_reference.load('classroom-root')
    context = {
        'classroom_list': Classroom.objects.enrolled(request.user),
        'navbar': navbar_list(root, request.user),
    }
    return render(request, 'classrooms/list.jinja2', context)


@login_required
def classroom_detail(request, slug):
    classroom = get_object_or_404(Classroom, slug=slug)
    enrolled = is_registered(request.user, classroom)
    context = {
        'classroom': classroom,
        'page': classroom,
        'navbar': navbar_classroom(classroom, request.user),
        'enrolled': enrolled,
    }
    if not enrolled:
        context['form'] = form = EnrollForm(request.POST)
        if form.is_valid_for(classroom):
            classroom.enroll_student(request.user)
            context['enrolled'] = True

    return render(request, 'classrooms/detail.jinja2', context)


@login_required
def enroll_in_classroom(request):
    context = {
        'classroom_list': Classroom.objects.can_enroll(request.user),
        'navbar': navbar_list(None, request.user),
    }
    return render(request, 'classrooms/enroll.jinja2', context)
