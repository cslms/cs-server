from django.conf.urls import url

from . import views

#
#
# def merged_dict(dict_a, dict_b):
#     """Merges two dicts and returns output. It's purpose is to ease use of
#     ``auth_views_compat_quirks``
#     """
#
#     dict_a.update(dict_b)
#     return dict_a
#
#
# def setting_success_url(func, url, keywords):
#     """
#     Revert success url and apply to func.
#     """
#
#     def decorated(request, *args, **kwargs):
#         success_url = reverse(url, kwargs={
#             k: v for k, v in kwargs.items() if k in keywords
#             })
#         kwargs['success_url'] = success_url
#         return func(request, *args, **kwargs)
#
#     return decorated
#
#

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]

#     # Signup, signin and signout
#     url(r'^logout/$',
#         userena_views.signout,
#         {
#             'template_name': 'auth/signout.jinja2'
#         },
#         name='signout'),
#
#     # Reset password
#     # url(r'^password/reset/$',
#     #     auth_views.password_reset,
#     #     merged_dict({'template_name': 'userena/password_reset_form.html',
#     #                  'email_template_name': 'userena/emails/password_reset_message.txt',
#     #                  'extra_context': {
#     #                      'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES}
#     #                  }, auth_views_compat_quirks['userena_password_reset']),
#     #     name='userena_password_reset'),
#     # url(r'^password/reset/done/$',
#     #     auth_views.password_reset_done,
#     #     {'template_name': 'userena/password_reset_done.html',},
#     #     name='userena_password_reset_done'),
#     # url(
#     #     r'^password/reset/confirm/(?P<%s>[0-9A-Za-z]+)-(?P<token>.+)/$' % password_reset_uid_kwarg,
#     #     auth_views.password_reset_confirm,
#     #     merged_dict(
#     #         {'template_name': 'userena/password_reset_confirm_form.html',
#     #          }, auth_views_compat_quirks['userena_password_reset_confirm']),
#     #     name='userena_password_reset_confirm'),
#     # url(r'^password/reset/confirm/complete/$',
#     #     auth_views.password_reset_complete,
#     #     {'template_name': 'userena/password_reset_complete.html'},
#     #     name='userena_password_reset_complete'),
#
#     # Signup
#     # url(r'^(?P<username>[\@\.\w-]+)/signup/complete/$',
#     #     userena_views.direct_to_user_template,
#     #     {'template_name': 'userena/signup_complete.html',
#     #      'extra_context': {
#     #          'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
#     #          'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
#     #     name='userena_signup_complete'),
#
#     # Activate
#     # url(r'^activate/(?P<activation_key>\w+)/$',
#     #     userena_views.activate,
#     #     name='userena_activate'),
#
#     # Retry activation
#     # url(r'^activate/retry/(?P<activation_key>\w+)/$',
#     #     userena_views.activate_retry,
#     #     name='userena_activate_retry'),
#
#     # Change email and confirm it
#     url(r'^(?P<username>[\@\.\w-]+)/email/$',
#         userena_views.email_change,
#         name='userena_email_change'),
#     url(r'^(?P<username>[\@\.\w-]+)/email/complete/$',
#         userena_views.direct_to_user_template,
#         {'template_name': 'userena/email_change_complete.html'},
#         name='userena_email_change_complete'),
#     url(r'^(?P<username>[\@\.\w-]+)/confirm-email/complete/$',
#         userena_views.direct_to_user_template,
#         {'template_name': 'userena/email_confirm_complete.html'},
#         name='userena_email_confirm_complete'),
#     url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
#         userena_views.email_confirm,
#         name='userena_email_confirm'),
#
#     # Disabled account
#     # url(r'^(?P<username>[\@\.\w-]+)/disabled/$',
#     #     userena_views.disabled_account,
#     #     {'template_name': 'userena/disabled.html'},
#     #     name='userena_disabled'),
#
#     # Change password
#     url(r'^(?P<username>[\@\.\w-]+)/password/$',
#         setting_success_url(
#             userena_views.password_change,
#             url='auth:password-change-complete',
#             keywords={'username'},
#         ),
#         {
#             'template_name': 'auth/password-change.jinja2'
#         },
#         name='password-change'),
#     url(r'^(?P<username>[\@\.\w-]+)/password/complete/$',
#         userena_views.direct_to_user_template,
#         {
#             'template_name': 'auth/password-complete.jinja2'
#         },
#         name='password-change-complete'),
#
#     # Edit profile
#     url(r'^(?P<username>[\@\.\w-]+)/edit/$',
#         setting_success_url(
#             userena_views.profile_edit, 'auth:profile-detail', {'username'}
#         ),
#         {
#             'template_name': 'auth/profile-edit.jinja2',
#             'edit_profile_form': forms.EditProfileForm,
#         },
#         name='profile-edit'),
#
#     # View profiles
#     url(r'^(?P<username>(?!(signout|signup|signin)/)[\@\.\w-]+)/$',
#         userena_views.profile_detail,
#         {
#             'template_name': 'auth/profile-detail.jinja2'
#         },
#         name='profile-detail'),
#     url(r'^page/(?P<page>[0-9]+)/$',
#         userena_views.ProfileListView.as_view(
#             template_name='auth/profile-list.jinja2'
#         ),
#         name='profile-list-paginated'),
#     url(r'^$',
#         userena_views.ProfileListView.as_view(),
#         name='profile-list'),
# ]
