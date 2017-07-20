import random
from .models import User
from social_core.pipeline.partial import partial
from django.shortcuts import render

USER_FIELDS = ['alias', 'email', 'school_id']

def set_temp_school_id(email):
    return email[:20]

def create_user(strategy, details, backend, request=None, user=None, *args, **kwargs):

    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    fields['alias'] = details['username']
    fields['school_id'] = set_temp_school_id(fields['email'])

    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
