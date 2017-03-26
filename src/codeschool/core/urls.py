from django.conf.urls import url

from codeschool.core.views import debug_page_view


urlpatterns = [
    url(r'^$', debug_page_view, name='cs-debug'),
]
