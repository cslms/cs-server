"""
Django settings for server project.
"""
import sys

import os

from . import _paths as paths
from . import _secrets as secrets
from ._debug import DEBUG

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

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
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'codeschool.urls'

WSGI_APPLICATION = 'codeschool.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(paths.DB_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(paths.DB_DIR, 'testdb.sqlite3'),
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
    paths.FRONTEND_BUILD_DIR,
    paths.ROOT_FILES_DIR,
]

STATIC_ROOT = paths.STATIC_DIR
MEDIA_ROOT = paths.MEDIA_DIR
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
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)
ANONYMOUS_USER_ID = 1
AUTH_USER_MODEL = 'users.User'
AUTH_PROFILE_MODULE = 'accounts.Profile'

# Social authentication

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/auth/login/'

# OAUTH keys (not working yet, should read from secrets!)

keys = secrets.OAUTH_KEYS
secret_keys = secrets.OAUTH_SECRET_KEYS

SOCIAL_AUTH_GITHUB_KEY = secrets.key_handler(keys, 'github')
SOCIAL_AUTH_GITHUB_SECRET = secrets.key_handler(secret_keys, 'github')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secrets.key_handler(keys, 'google-oauth2')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secrets.key_handler(secret_keys, 'google-oauth2')
SOCIAL_AUTH_FACEBOOK_KEY = secrets.key_handler(keys, 'facebook')
SOCIAL_AUTH_FACEBOOK_SECRET = secrets.key_handler(secret_keys, 'facebook')
SOCIAL_AUTH_TWITTER_KEY = secrets.key_handler(keys, 'twitter')
SOCIAL_AUTH_TWITTER_SECRET = secrets.key_handler(secret_keys, 'twitter')

# Social OAuth scopes

SOCIAL_AUTH_TWITTER_SCOPE = ['user']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_GITHUB_SCOPE = ['user']
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

#OAuth pipeline

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'codeschool.core.users.oauth_pipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Accounts and users


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

# REST Framework

REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Tries to detect if it is running on a test session

IS_RUNNING_TESTS = (
    sys.argv[0].endswith('py.test') or sys.argv[0].endswith('pytest') or
    os.environ.get('IS_TESTING', 'false') == 'true' or
    'test' in sys.argv
)
if IS_RUNNING_TESTS:
    print('Running tests and disabling sandboxed execution')
