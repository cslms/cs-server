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
        name='auth-login',
    ),
    url(
        r'^auth/logout/$',
        views.logout,
        name='auth-logout',
    ),
    url(
        r'^auth/password/$',
        views.change_password,
        name='auth-change-password',
    ),
    url(
        r'^auth/email/$',
        views.change_email,
        name='auth-change-email',
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
