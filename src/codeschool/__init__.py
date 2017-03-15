"""
Overview of codeschool codebase:

Packages

- auth: user authentication, login and signup (uses userena)
- components: jinja2/pyml components
- core: a mixed bag of core functionality
- extra: optional codeschool activities
- fixes: monkey-patch 3rd party libs
- gamification: points, badges and stars
- lms: learning management system, control courses, grades, etc
- questions: implement different question types
- settings: django settings
- site: core templates
- social: social network capabilities
- tests: global tests
- vendor: vendorized libs
"""

from .__meta__ import __author__, __version__

# Import useful functions
from codeschool.core import sys_page, rogue_root, hidden_root, wagtail_root, config


# Redis support
import redis as _redis
redis = _redis.connection.Connection()
try:
    redis.connect()
except _redis.ConnectionError:
    from subprocess import check_call as _run, CalledProcessError
    from time import time

    try:
        _run(['redis-server', '--daemonize', 'yes'])
    except CalledProcessError:
        raise RuntimeError(
            'Redis is not installed. Please install and Redis and make it '
            'runable from the redis-server command or initialize the redis '
            'server before starting codeschool.')

    # We have 1s to connect to redis server
    _tf = time() + 1.0
    while time() < _tf:
        try:
            redis.connect()
        except _redis.ConnectionError:
            pass
    else:
        redis.connect()

# Celery support
# from .celery import app as celery_app
