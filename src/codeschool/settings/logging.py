import os
from codeschool.settings import DEBUG

cd = os.path.dirname
base = cd(cd(cd(cd(__file__))))
LOGDIR = os.path.join(base, 'log')
LOGFILE_INFO = os.path.join(LOGDIR, 'info.log')
LOGFILE_WARNINGS = os.path.join(LOGDIR, 'warnings.log')
DEFAULT_HANDLERS = ['file', 'file-info', 'console']

# Force existence of a log/ directory
if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(name)-40s %(process)-5d %(thread)-2d [ %(levelname)-8s ] %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(name)-40s [ %(levelname)-8s ] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file-info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': LOGFILE_INFO,
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOGFILE_WARNINGS,
        },

    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'propagate': True,
        },
        'codeschool': {
            'handlers': DEFAULT_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
        'boxed': {
            'handlers': DEFAULT_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
        'ejudge': {
            'handlers': DEFAULT_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


del cd, base, os
