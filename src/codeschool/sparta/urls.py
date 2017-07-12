from django.conf.urls import include, url
from . import views

# Basic URLS
urlpatterns = [
    url(r'^$', views.index, name='sparta_index'),
    url(r'^activities$', views.activities, name='sparta_activities'),
    url(r'^membersrating$', views.rating, name='sparta_rating'),
]
