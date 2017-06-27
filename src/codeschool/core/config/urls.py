from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.debug_page_view, name='cs-debug'),
]
