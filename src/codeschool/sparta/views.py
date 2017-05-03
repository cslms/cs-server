from django.shortcuts import render
from bricks.contrib.mdl import button, div

# Create your views here.
def index(request):
    
    ctx = {'content_body':div(button('click me', primary=True), shadow=2), 'content_title':'Hey!'}
    return render(request, 'sparta/index.jinja2', ctx)
