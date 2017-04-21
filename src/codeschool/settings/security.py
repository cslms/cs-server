# SECURITY WARNING: keep the secret key used in production secret!

import os
import random
import string
choice = random.SystemRandom().choice

d = os.path.dirname
base_dir = d(d(d(d(os.path.abspath(__file__)))))
security_path = os.path.join(base_dir, 'security')
secrete_key_path = os.path.join(security_path, 'secret_key.dat')

try:
    with open(secrete_key_path, 'r') as F:
        SECRET_KEY = F.read()

except FileNotFoundError:
    print('Creating a new SECRET_KEY at security/secret_key.dat')

    # Create directory, if it does not exist
    if not os.path.exists(security_path):
        os.mkdir(security_path)

    chars = ''.join([string.ascii_letters, string.digits, string.punctuation])
    SECRET_KEY = ''.join([choice(chars) for i in range(50)])

    with open(secrete_key_path, 'w') as F:
        SECRET_KEY = F.write(SECRET_KEY)


# Check if db directory exists so database can be created
db_dir = os.path.join(base_dir, 'db')
if not os.path.exists(db_dir):
    os.mkdir(db_dir)
