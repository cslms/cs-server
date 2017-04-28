"""
Django settings for server project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# This is <repo>/src/codeschool/
import sys

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)
SRC_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(SRC_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.environ.get('CODESCHOOL_PRODUCTION', False) != 'true'
if not DEBUG:
    ALLOWED_HOSTS = ['localhost', 'codeschool']

# Application definition

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'codeschool.urls'

WSGI_APPLICATION = 'codeschool.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DB_DIR = os.path.join(REPO_DIR, 'db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(DB_DIR, 'testdb.sqlite3'),
        }

    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(REPO_DIR, 'static'),
]

COLLECT_DIR = os.path.join(REPO_DIR, 'collect')
STATIC_ROOT = os.path.join(COLLECT_DIR, 'static')
MEDIA_ROOT = os.path.join(COLLECT_DIR, 'media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Django compressor

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_PRECOMPILERS = [
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
    ('text/stylus', 'stylus < {infile} > {outfile}'),
]

# Wagtail
# http://docs.wagtail.io/en/latest/getting_started/integrating_into_django.html

WAGTAIL_SITE_NAME = 'Codeschool'

# Authentication

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ANONYMOUS_USER_ID = 1
AUTH_PROFILE_MODULE = 'accounts.Profile'

# Social authentication

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/auth/login/'

# OAUTH keys (not working yet)

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ''
SOCIAL_AUTH_FACEBOOK_KEY = '1085127354890672'
SOCIAL_AUTH_FACEBOOK_SECRET = '9f6ba5c8721172acaf25a733c4c81a99'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_TWITTER_KEY = 'JrIVXbXZguPeUsnqcjtbQEWXH'
SOCIAL_AUTH_TWITTER_SECRET = 'vMZjdO7DsUV8mVo46smQK2SHyhCxnXyc24gxH6J6cH08anWqHA'

# Userena support

USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_ACTIVATION_DAYS = 7
USERENA_FORBIDDEN_USERNAMES = (
    'signup', 'signout', 'signin', 'activate', 'me', 'password', 'login',
    'codeschool'
)
USERENA_USE_HTTPS = False
USERENA_REGISTER_PROFILE = False
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_PROFILE_LIST_TEMPLATE = 'auth/profile-list.jinja2'

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/signout/'
SITE_ID = 1

# Cache framework

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:6379/1' % os.environ.get('REDIS_SERVER',
                                                         'localhost'),
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
}

# Django sessions

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Celery settings

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Tries to detect if it is running on a test session

IS_RUNNING_TESTS = (
    sys.argv[0].endswith('py.test') or sys.argv[0].endswith('pytest') or
    os.environ.get('IS_TESTING', 'false') == 'true' or
    'test' in sys.argv
)
if IS_RUNNING_TESTS:
    print('Running tests and disabling sandboxed execution')
