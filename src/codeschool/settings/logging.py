import os
from codeschool.settings import DEBUG

# Force existence of a log/ directory
if not os.path.exists('log'):
    os.mkdir('log')

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
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': 'log/cs.log',
        },

    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'propagate': True,
        },
        'codeschool': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'boxed': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'ejudge': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
