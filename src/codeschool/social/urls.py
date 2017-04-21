from django.conf.urls import url

from codeschool.social.feed.views import timeline_view, feed_view
from codeschool.social.friends.views import friends_view, add_friends_view


urlpatterns = [
    url(r'^timeline/$', timeline_view, name='timeline'),
    url(r'^feed/$', feed_view, name='feed'),
    url(r'^friends/$', friends_view, name='friends'),
    url(r'^friends/add/$', add_friends_view, name='friends-add'),
]
