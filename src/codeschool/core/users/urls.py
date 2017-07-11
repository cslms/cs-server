from django.conf.urls import url

from . import views

#
# The urlpatterns for the codeschool.core.users app are mounted directly in the
# root url.
#
urlpatterns = [
    url(
        r'^login/$',
        views.start,
        name='login',
    ),
    url(
        r'^auth/logout/$',
        views.logout,
        name='logout',
    ),
    url(
        r'^auth/password/$',
        views.change_password,
        name='change-password',
    ),
    url(
        r'^auth/email/$',
        views.change_email,
        name='change-email',
    ),
    url(
        r'profile/$',
        views.current_user_profile,
        name='users-profile',
    ),
    url(
        r'profile/edit/$',
        views.edit_profile,
        name='users-edit-profile',
    ),
    url(
        r'profile/(?P<pk>[0-9]+)/$',
        views.user_profile,
        name='users-view-profile',
    ),
]
