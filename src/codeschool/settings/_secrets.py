# SECURITY WARNING: keep the secret keys used in production secret!


import json
import string

import os
import random

from ._paths import LOCAL_DIR

choice = random.SystemRandom().choice

secrets_path = os.path.join(LOCAL_DIR, 'secrets.json')
oauth_key_path = os.path.join(LOCAL_DIR, 'oauth_keys.json')
data = {}
key = {}

# SECRET SYSTEM KEY

try:
    with open(secrets_path, 'r') as F:
        data = json.load(F)
        SECRET_KEY = data['secret-key']

except (FileNotFoundError, KeyError) as e:
    print('Creating a new secrets file at local/secrets.json')

    chars = ''.join([string.ascii_letters, string.digits, string.punctuation])
    SECRET_KEY = ''.join([choice(chars) for i in range(50)])
    data['secret-key'] = SECRET_KEY

    with open(secrets_path, 'w') as F:
        json.dump(data, F)

# OAUTH KEYS

try:

    chars = ''.join([string.ascii_letters, string.digits, string.punctuation])
    OAUTH_DEFAULT_KEY = ''.join([choice(chars) for i in range(20)])

    with open(oauth_key_path, 'r') as K:
        key = json.load(K)

        OAUTH_KEYS = key['keys']
        OAUTH_SECRET_KEYS = key['secret_keys']

        OAUTH_KEYS['default'] = OAUTH_DEFAULT_KEY
        OAUTH_SECRET_KEYS['default'] = OAUTH_DEFAULT_KEY

except (FileNotFoundError, KeyError) as e:
    print('There was an error while parsing the OAuth Keys')

    OAUTH_KEYS = {'default': OAUTH_DEFAULT_KEY}
    OAUTH_SECRET_KEYS = {'default': OAUTH_DEFAULT_KEY}

def key_handler(data, key):
        try:
            return data[key]
        except (KeyError) as e:
            return data['default']
