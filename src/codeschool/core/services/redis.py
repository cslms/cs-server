# Redis support
#
# This script checks for a valid Redis connection and tries to initialize the
# redis-server if no connection is found.
#
# These steps are only necessary in development. Production should initialize
# the redis server explicitly.
#

from codeschool import settings

if settings.DEBUG:
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
