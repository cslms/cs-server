"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os

from django.conf.urls import url, include
from wagtail.wagtailcore import urls as wagtail_urls

from codeschool import settings
from codeschool.accounts.views import profile_view
from codeschool.api import router
from codeschool.core.views import index_view

# Basic URLS
urlpatterns = [
    url(r'^admin/', include('wagtail.wagtailadmin.urls')),
    url(r'^$', index_view, name='index'),
    url(r'^profile/$', profile_view, name='profile-view'),
    url(r'^auth/', include('codeschool.accounts.urls', namespace='auth')),
]

# Optional debug views
if settings.CODESCHOOL_DEBUG_VIEWS or settings.DEBUG:
    import django.contrib.admin

    urlpatterns += [
        url(r'^_admin/', django.contrib.admin.site.urls),
        url(r'^_debug/', include('codeschool.core.urls')),
        url(r'^_bricks/', include('codeschool.bricks.urls')),
    ]

# Optional "social" urls
if 'codeschool.social' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^social/', include('codeschool.social.urls', namespace='social')),
    ]

# Global questions list
if settings.CODESCHOOL_GLOBAL_QUESTIONS:
    from codeschool.lms.activities.views import main_question_list

    urlpatterns += [
        url(r'^questions/$', main_question_list, name='question-list'),
    ]

# Codeschool classrooms
if 'codeschool.lms.classrooms' in settings.INSTALLED_APPS:
    from codeschool.lms.classrooms import urls as classrooms_urls

    urlpatterns += [
        url(r'^classes/', include(classrooms_urls, namespace='classrooms')),
    ]

# Optional cli/clt interface
if 'codeschool.cli' in settings.INSTALLED_APPS:
    from codeschool.cli import api as jsonrpc_api

    urlpatterns += [
        url(r'^cli/jsonrpc/', include(jsonrpc_api.urls)),
    ]

# Django serves static urls for the dev server.
# Production relies on Nginx.
if os.environ.get('DJANGO_SERVE_STATIC', False) or settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

# REST framework urls:
# We have to put those urls in the end of the file since each app must import
# the router and include its viewsets
if settings.CODESCHOOL_REST_API:
    import codeschool.lms.activities.api

    codeschool.lms.activities.api.register(router)

    urlpatterns += [
        url(r'^api/', include(router.urls)),
        url(r'^api/auth/', include('rest_framework.urls', namespace='rest-auth')),
    ]

# Wagtail endpoint (these must be last)
urlpatterns += [
    wagtail_urls.urlpatterns[0],
    url(r'^((?:[\w\-\.]+/)*)$',
        wagtail_urls.views.serve, name='wagtail_serve'),
    url(r'^((?:[\w\-\.]+/)*[\w\-\.]+\.(?:bricks|json|api)/?)$',
        wagtail_urls.views.serve, name='wagtail-api-serve'),
]
