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

from django.apps import apps
from django.conf.urls import url, include
from wagtail.wagtailcore import urls as wagtail_urls

from . import settings
from .api import router, import_api_modules
from .core.config.views import index_view
from .core.users.views import start_view

import_api_modules()

# Basic URLS
urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^login/$', start_view, name='login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest-auth')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include('wagtail.wagtailadmin.urls')),
]

# Optional debug views
if settings.CODESCHOOL_DEBUG_VIEWS or settings.DEBUG:
    import django.contrib.admin
    from .core.config.views import debug_page_view

    urlpatterns += [
        url(r'^_admin/',
            django.contrib.admin.site.urls),
        url(r'^_debug/',
            debug_page_view, name='config-debug-page'),
        url(r'^_bricks/',
            include('codeschool.bricks.urls', namespace='bricks')),
    ]

# Optional "social" urls
if apps.is_installed('codeschool.social'):
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
if apps.is_installed('codeschool.lms.classrooms'):
    from codeschool.lms.classrooms import urls as classrooms_urls

    urlpatterns += [
        url(r'^classes/', include(classrooms_urls, namespace='classrooms')),
    ]

# Optional cli/clt interface
if apps.is_installed('codeschool.cli'):
    from codeschool.cli import api as jsonrpc_api

    urlpatterns += [
        url(r'^cli/jsonrpc/', include(jsonrpc_api.urls)),
    ]

# Django serves static urls for the dev server.
# Production relies on Nginx.
if os.environ.get('DJANGO_SERVE_STATIC', False) or settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

# Wagtail endpoint (these must be last)
urlpatterns += [
    wagtail_urls.urlpatterns[0],
    url(r'^((?:[\w\-\.]+/)*)$',
        wagtail_urls.views.serve, name='wagtail_serve'),
    url(r'^((?:[\w\-\.]+/)*[\w\-\.]+\.(?:bricks|json|api)/?)$',
        wagtail_urls.views.serve, name='wagtail-api-serve'),
]
