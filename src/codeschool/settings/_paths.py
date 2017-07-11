"""
Manage all important codeschool paths.
"""

import os

join = os.path.join
dirname = os.path.dirname


def assure_path(path):
    """
    Create all parent paths until given path exists.
    """

    if not path:
        raise ValueError('empty paths are invalid')

    if not os.path.exists(path):
        base, name = os.path.split(path)
        assure_path(base)
        print('INFO: Creating %s/%s/' % (base, name))
        os.mkdir(path)


def safe_join(*args):
    """
    Join path parts and create directory if it does not exist.
    """

    path = join(*args)
    assure_path(path)
    return path


# ------------------------------------------------------------------------------
# Define constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# This is <repo>/src/codeschool/
SETTINGS_DIR = dirname(os.path.abspath(__file__))
LOCAL_SETTINGS_PATH = join(SETTINGS_DIR, 'local.py')
BASE_DIR = dirname(SETTINGS_DIR)
SRC_DIR = dirname(BASE_DIR)
REPO_DIR = dirname(SRC_DIR)

# Local dirs
LOCAL_DIR = safe_join(REPO_DIR, 'local')
DB_DIR = safe_join(LOCAL_DIR, 'db')
VOLUMES_DIR = safe_join(LOCAL_DIR, 'volumes')
SOCK_DIR = safe_join(LOCAL_DIR, 'sock')
BACKUP_DIR = safe_join(LOCAL_DIR, 'backup')
LOG_DIR = safe_join(LOCAL_DIR, 'log')

cd = os.path.dirname
base = cd(cd(cd(cd(__file__))))
LOGDIR = os.path.join(base, 'log')
LOGFILE_INFO_PATH = os.path.join(LOGDIR, 'info.log')
LOGFILE_WARNINGS_PATH = os.path.join(LOGDIR, 'warnings.log')

# Force existence of a log/ directory
if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)

# Frontend dirs
FRONTEND_DIR = join(REPO_DIR, 'frontend')
JS_BUILD_DIR = join(FRONTEND_DIR, 'js')
ROOT_FILES_DIR = join(FRONTEND_DIR, 'root-files')
FRONTEND_SRC_DIR = join(FRONTEND_DIR, 'src')
FRONTEND_SCSS_DIR = join(FRONTEND_SRC_DIR, 'scss')
FRONTEND_JS_DIR = join(FRONTEND_SRC_DIR, 'js')
FRONTEND_BUILD_DIR = join(FRONTEND_DIR, '_build')
COLLECT_DIR = join(FRONTEND_BUILD_DIR, 'collect')
STATIC_DIR = join(FRONTEND_BUILD_DIR, 'static')
MEDIA_DIR = join(FRONTEND_BUILD_DIR, 'media')

# Create local configuration if it does not exist
if not os.path.exists(LOCAL_SETTINGS_PATH):
    data = """# Local configuration file that can be personalized by each developer.

from .dev import *
"""
    with open(LOCAL_SETTINGS_PATH, 'w') as F:
        F.write(data)
