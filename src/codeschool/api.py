import importlib
import logging

from django.apps import apps
from rest_framework.routers import DefaultRouter

log = logging.getLogger(__name__)

# Default router for the REST api. Apps should load this object and register
# viewsets for each API endpoint.
router = DefaultRouter()


def import_api_modules():
    """
    Import the .api module for all apps implemented under the codeschool
    namespace.
    """

    for app in apps.get_app_configs():
        if app.module.__name__.startswith('codeschool'):
            api_module = app.module.__name__ + '.api'
            try:
                importlib.import_module(api_module)
            except ImportError:
                pass
            else:
                log.debug('imported module: %s' % api_module)
