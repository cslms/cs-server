from django.conf.urls import url

from codeschool.social.feed.views import timeline_view, feed_view


urlpatterns = [
    url(r'^timeline/$', timeline_view, name='timeline'),
    url(r'^feed/$', feed_view, name='feed'),
]
