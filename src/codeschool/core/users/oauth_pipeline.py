import random
from .models import User
from IPython import embed

USER_FIELDS = ['alias', 'email', 'school_id']

def set_random_school_id():
    school_id = str(random.randint(0, (10**21)-1))

    while(User.objects.filter(school_id = school_id).count() != 0):
        school_id = str(random.randint(0, (10**21)-1))

    return school_id

def create_user(strategy, details, backend, user=None, *args, **kwargs):

    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    fields['alias'] = details['username']


    fields['school_id'] = set_random_school_id()

    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
