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
from codeschool.core.views import index_view

# Basic URLS
urlpatterns = [
    url(r'^admin/', include('wagtail.wagtailadmin.urls')),
    url(r'^$', index_view),
    url(r'^profile/$', profile_view, name='profile-view'),
    url(r'^auth/', include('codeschool.accounts.urls', namespace='auth')),
]

# Optional debug views
if settings.CODESCHOOL_DEBUG_VIEWS:
    import django.contrib.admin

    urlpatterns += [
        url(r'^_admin/', django.contrib.admin.site.urls),
        url(r'^_debug/', include('codeschool.core.urls')),
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

# Courses interface
if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
    from codeschool.lms.courses.views import course_list

    urlpatterns += [
        url(r'^courses/$', course_list, name='course-list'),
    ]

# Wagtail endpoint (these must come last)
urlpatterns += [
    wagtail_urls.urlpatterns[0],
    url(r'^((?:[\w\-\.]+/)*)$', wagtail_urls.views.serve, name='wagtail_serve'),
    url(r'^((?:[\w\-\.]+/)*[\w\-\.]+\.(?:srvice|json|api)/?)$', wagtail_urls.views.serve, name='wagtail-api-serve'),
]

# Django serves static urls for the dev server.
# Production relies on Nginx.
if os.environ.get('DJANGO_SERVE_STATIC', True):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()