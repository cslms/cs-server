from django import http
from django.apps import apps
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import viewsets

from . import config_options
from . import models
from . import serializers
from .debug_info import DebugInfo


def index_view(request):
    """
    Simple index view. Redirect to login or to user profile page.
    """

    initial = config_options.get('initial-page', None)
    if initial is None:
        if apps.is_installed('codeschool.extra.fresh_install'):
            from codeschool.extra.fresh_install.views import \
                configure_server_view
            return configure_server_view(request)
        else:
            return http.HttpResponseBadRequest('initial-page is not set!')

    if request.user.is_anonymous():
        return redirect('auth:login')

    return redirect(config_options['initial-page'])


def debug_page_view(request):
    """
    Shows debug information about codeschool.
    """

    info = DebugInfo(user=request.user)
    return render(request, 'config/debug.jinja2', dict(info))


class DataEntryKeyValuePairViewSet(viewsets.ModelViewSet):
    """
    Advanced interface for configurable server data.
    """

    queryset = models.DataEntryKeyValuePair.objects.all()
    serializer_class = serializers.DataEntryKeyValuePair


class ConfigOptionKeyValuePairViewSet(viewsets.ModelViewSet):
    """
    Advanced interface for configurable server options.
    """

    queryset = models.ConfigOptionKeyValuePair.objects.all()
    serializer_class = serializers.ConfigOptionKeyValuePairSerializer
