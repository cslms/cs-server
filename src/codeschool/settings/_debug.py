# A simple file that controls the SETTINGS DEBUG variable. It exposes
# two functions set_debug() and get_debug()

import os

DEBUG = os.environ.get('DEBUG', 'false').lower() in ['true', 't', '1']


def get_debug():
    return DEBUG


def set_debug(value):
    global DEBUG
    DEBUG = bool(value)
