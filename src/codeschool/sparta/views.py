from django.shortcuts import render
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout

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
        'content_body': ul(class_="cs-sparta-list")[
            li(a('Atividade 1', href='#')),
            li(a('Atividade 2', href='#')),
            li(a('Atividade 3', href='#')),
        ]
    }
    return render(request, 'sparta/activities.jinja2', ctx)