from django.conf.urls import url
from django.shortcuts import render

from bricks.components.html5_tags import div, h2, a, ul, li
from . import views


def index_view(request):
    urls = []
    for item in list(urlpatterns)[1:]:
        name = item._regex[1:-1]
        urls.append(a(name.title(), href=name))

    ctx = {
        'content_title': 'Codeschool components overview',
        'content_body': div()[
            h2('List of components'),
            ul(map(li, urls))
        ],
    }
    return render(request, 'base.jinja2', ctx)


urlpatterns = [
    url(r'^$', index_view),
    url(r'^navbar$', views.navbar_view),
    url(r'^iospec$', views.iospec_view),
    url(r'^cards$', views.cards_view),
    url(r'^feedback$', views.feedback_view),
    url(r'^submissions$', views.submissions_view),
]
