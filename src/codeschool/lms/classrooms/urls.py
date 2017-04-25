from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.list_view, name='list'),
    url(r'^(?P<slug>[-\w]+)/$', views.detail_view, name='list'),
]
