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

import django.contrib.admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wagtail.wagtailcore import urls as wagtail_urls

from codeschool.auth.views import profile_view
from codeschool.core.views import index_view
from codeschool.lms.activities.views import main_question_list
from codeschool.lms.courses.views import course_list


urlpatterns = [
    # Basic URLS
    url(r'^_admin/', django.contrib.admin.site.urls),
    url(r'^admin/', include('wagtail.wagtailadmin.urls')),
    url(r'^$', index_view),
    url(r'^profile/$', profile_view, name='profile-view'),

    # Codeschool Apps
    url(r'^auth/', include('codeschool.auth.urls', namespace='auth')),
    url(r'^social/', include('codeschool.social.urls', namespace='social')),
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Global dashboard and objects
    url(r'^questions/$', main_question_list, name='question-list'),
    url(r'^courses/$', course_list, name='course-list'),

    # Debugging
    url(r'^_debug/', include('codeschool.core.urls')),

    # Wagtail endpoint
    wagtail_urls.urlpatterns[0],
    url(r'^((?:[\w\-\.]+/)*)$', wagtail_urls.views.serve, name='wagtail_serve'),
    url(r'^((?:[\w\-\.]+/)*[\w\-\.]+\.(?:srvice|json|api)/?)$', wagtail_urls.views.serve, name='wagtail-api-serve'),
]

# Django serves static urls. Should not be used in production: production
# should rely on nginx, apache or any other proxy server.
if os.environ.get('DJANGO_SERVE_STATIC', True):
    urlpatterns += staticfiles_urlpatterns()
