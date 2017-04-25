import model_reference
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Classroom


@login_required
def list_view(request):
    """
    List of classroom pages.
    """

    root = model_reference.load('classroom-root')
    context = {'classroom_list': Classroom.objects.enrolled(request.user)}
    return render(request, 'classrooms/list.jinja2', context)


@login_required
def detail_view(request, slug):
    """
    Course details.
    """
    classroom = get_object_or_404(Classroom, slug=slug)
    context = {
        'classroom': classroom,
        'page': classroom,
    }
    return render(request, 'classrooms/detail.jinja2', context)
