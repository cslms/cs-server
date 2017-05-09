# Redis support
#
# This script checks for a valid Redis connection and tries to initialize the
# redis-server if no connection is found.
#
# These steps are only necessary in development. Production should initialize
# the redis server explicitly.
#
import os

from codeschool import settings


def start_redis_and_connect(redis):
    from subprocess import check_call as _run, CalledProcessError
    from time import time
    import redis as _redis

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


def redis_connect():
    import redis as _redis

    redis = _redis.connection.Connection()
    try:
        redis.connect()
    except _redis.ConnectionError:
        start_redis_and_connect(redis)


if settings.DEBUG:
    redis_connect()
