from django.core.exceptions import ImproperlyConfigured

from codeschool import settings

# Makes sure dependencies are right
if 'codeschool.social' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'Please install codeschool.social app in order to use '
        'codeschool.lms.courses.'
    )
