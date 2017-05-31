from django.shortcuts import render
from bricks.contrib.mdl import button, div
from .bricks import navbar, layout

# Create your views here.
def index(request):
    
    ctx = {
        'main':layout(), 
        'navbar':navbar(),
    }
    return render(request, 'sparta/index.jinja2', ctx)
