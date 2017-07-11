# SECURITY WARNING: keep the secret key used in production secret!

import json
import string

import os
import random

from ._paths import LOCAL_DIR

choice = random.SystemRandom().choice

secrets_path = os.path.join(LOCAL_DIR, 'secrets.json')
data = {}

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
