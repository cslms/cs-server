from django.shortcuts import render
from django.contrib.auth.models import User
from bricks.contrib.mdl import button, div
from django.http import HttpResponse
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout, rating_layout
from .models.activity import UserRating

# Create your views here.
def index(request):

    ctx = {
    'main':layout(request.user),
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
        user_rating = None
        try:
            user_rating = UserRating.objects.get(
                user_evaluated=User.objects.get(pk=request.POST['user_evaluated']),
                user_evaluatee=request.user
            )
            user_rating.rating = request.POST['rating']
            user_rating.save()
        except:
            user_rating = UserRating()
            user_rating.user_evaluated = User.objects.get(pk=request.POST['user_evaluated'])
            user_rating.user_evaluatee = request.user
            user_rating.rating = request.POST['rating']
            try:
                user_rating.save()
                return HttpResponse(status=201)
            except:
                return HttpResponse(status=400)

    ctx = {
        'content_title':'Avaliação dos Membros',
        'content_body': rating_layout(request.user),
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