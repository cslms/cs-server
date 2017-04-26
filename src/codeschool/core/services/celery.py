# Celery support
#
# This script checks for a valid Celery worker with rabbitMQ and tries to
# initialize the rabbitMQ server if no connection is found.
#
# These steps are only necessary in development. Production should initialize
# the celery workers explicitly.
#

from codeschool import settings

if settings.DEBUG:
    print('TODO: Starting celery worker')
