from django.conf.urls import include, url
from . import views

# Basic URLS
urlpatterns = [
    url(r'^$', views.index, name='index'),
]