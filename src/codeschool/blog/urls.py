from django.conf.urls import include, url
from . import views

# Basic URLS
urlpatterns = [
    #url(r'^$', views.post_list, name='postlist'),
    url(r'^$', views.index, name='blog_index'), 
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_posts, name='userposts'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='postdetail'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='postedit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='postremove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='addcomment'),
	url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]
