from django.shortcuts import render
from bricks.contrib.mdl import button, div
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout, rating_layout
from .models import SpartaMembership, SpartaGroup

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
    if request.method == 'POST':
        membership = SpartaMembership.objects.get(pk=request.POST['member_ship'])
        membership.rating = request.POST['rate']

    membership = SpartaMembership.objects.get(user=request.user)
    group = membership.group
    members = group.members.all()

    ctx = {
        'content_title':'Avaliação dos Membros',
        'content_body': rating_layout(members),
        'script_links': [
            'userRating.js'
        ],
        'css_external_links': [
            'https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.3.2/'
            'jquery.rateyo.min.css'
        ],
        'script_external_links': [
            'https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.3.2/'
            'jquery.rateyo.min.js'
        ]
    }
    return render(request, 'sparta/rating.jinja2', ctx)
