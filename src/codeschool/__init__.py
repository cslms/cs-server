from .__meta__ import __author__, __version__
import sys

# Apply fixes
try:
    from codeschool import fixes as _fixes

    # Required services: Redis and Celery support
    if 'runserver' in sys.argv or 'runserver_plus' in sys.argv:
        import codeschool.core.services.redis as _redis
        import codeschool.core.services.celery as _celery
except ImportError:
    if 'python_boxed' not in sys.executable:
        raise

del sys
