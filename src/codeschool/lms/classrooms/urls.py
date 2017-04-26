from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.list_of_classrooms, name='list'),
    url(r'^enroll/$', views.enroll_in_classroom, name='list'),
    url(r'^(?P<slug>[-\w]+)/$', views.classroom_detail, name='list'),
]
