from django.conf.urls import url

from . import views

# Basic URLS
urlpatterns = [
    url(r'^$', views.push_question_ctl_view, name='question'),
]
