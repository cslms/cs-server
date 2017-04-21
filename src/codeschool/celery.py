import os
from django.conf import settings
from logging import getLogger
log = getLogger('codeschool.celery')

try:
    from celery import Celery
except ImportError:
    log.info('celery not loaded')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeschool.settings')
    app = Celery('codeschool')
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    log.info('celery started')
