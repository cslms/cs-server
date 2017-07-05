from django.shortcuts import render
from bricks.contrib.mdl import button, div
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout, rating_layout

# Create your views here.
def index(request):

    ctx = {
    'main':layout(),
    'navbar':navbar(),
    }
    return render(request, 'sparta/index.jinja2', ctx)

def activities(request):

    ctx = {
    'content_title':'Atividades',
    'content_body':activities_layout(),
    }
    return render(request, 'sparta/activities.jinja2', ctx)

def rating(request):

    ctx = {
        'content_title':'Avaliação dos Membros',
        'content_body': rating_layout()
    }
    return render(request, 'sparta/rating.jinja2', ctx)
