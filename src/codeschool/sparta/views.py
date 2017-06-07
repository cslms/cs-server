from django.shortcuts import render
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout

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
        'content_title':'Membros',
        'content_body': ul(class_="demo-list-icon mdl-list")[
            li(class_="mdl-list__item")[
            i(class_="material-icons mdl-list__item-icon")['person'],
            (a('Goku', href='#')),
            a(class_="mdl-list__item-secondary-action")(href='#')[i(class_="material-icons")['star']]
            ],
            li(class_="mdl-list__item")[
            i(class_="material-icons mdl-list__item-icon")['person'],
            (a('Ronaldo', href='#')),
            a(class_="mdl-list__item-secondary-action")(href='#')[i(class_="material-icons")['star']]
            ],
            li(class_="mdl-list__item")[
            i(class_="material-icons mdl-list__item-icon")['person'],
            (a('Florentina', href='#')),
            a(class_="mdl-list__item-secondary-action")(href='#')[i(class_="material-icons")['star']]
            ]
        ]
    }
    return render(request, 'sparta/rating.jinja2', ctx)
