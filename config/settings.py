import pathlib
import secrets
import sys

import environ
from django.conf.global_settings import LANGUAGES as BASE_LANGUAGES
from django.contrib import messages
from model_utils import Choices

from config.logging import LOGGING

ROOT_DIR = pathlib.Path(__file__).parent.parent
APPS_DIR = ROOT_DIR.joinpath('project')

sys.path.append(str(APPS_DIR.joinpath('apps')))

# pylint: disable=C0301

##############################################################################
# Default values for variables which should be present in .env file
##############################################################################

env = environ.Env(

    DJANGO_DEBUG=(bool, False),
    DJANGO_DEBUG_PROPAGATE_EXCEPTIONS=(bool, False),

    DJANGO_CSRF_USE_SESSIONS=(bool, True),
    DJANGO_SECRET_KEY=(str, secrets.token_urlsafe(50)),

    DJANGO_DATABASE_URL=(str, 'sqlite://'),

    DJANGO_CACHE=(str, 'locmemcache://'),

    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_DISALLOWED_USER_AGENTS=(list, []),
    DJANGO_INTERNAL_IPS=(list, []),
    DJANGO_DEFAULT_HTTP_PROTOCOL=(str, 'http'),

    DJANGO_ADMIN_URL=(str, 'admin/'),

    DJANGO_ADMINS=(list, []),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost'),
    DJANGO_EMAIL_URL=(str, 'consolemail://'),
    DJANGO_EMAIL_USE_LOCALTIME=(bool, True),
    DJANGO_EMAIL_SUBJECT_PREFIX=(str, 'Django'),
    DJANGO_EMAIL_SSL_CERTFILE=(str, ''),
    DJANGO_EMAIL_SSL_KEYFILE=(str, ''),

    DJANGO_DEFAULT_FILE_STORAGE=(str, 'django.core.files.storage.FileSystemStorage'),
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR.joinpath('static'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR.joinpath('media'))),

    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_DEBUG_SQL=(bool, False),
    DJANGO_DEBUG_SQL_COLOR=(bool, False),

    DJANGO_USE_SILK=(bool, False),
    DJANGO_SENTRY_DSN=(str, ''),
)

environ.Env.read_env()

##############################################################################
# Debugging
# https://docs.djangoproject.com/en/2.0/ref/settings/#debugging
##############################################################################

DEBUG = env.bool('DJANGO_DEBUG')

DEBUG_PROPAGATE_EXCEPTIONS = env.bool('DJANGO_DEBUG_PROPAGATE_EXCEPTIONS')

##############################################################################
# Security
# https://docs.djangoproject.com/en/2.0/ref/settings/#security
##############################################################################

CSRF_USE_SESSIONS = env.bool('DJANGO_CSRF_USE_SESSIONS')

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

##############################################################################
# Sites
# https://docs.djangoproject.com/en/2.0/ref/settings/#sites
##############################################################################

SITE_ID = 1

##############################################################################
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#database
##############################################################################

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL')
}

##############################################################################
# Cache
# https://docs.djangoproject.com/en/2.0/ref/settings/#cache
##############################################################################

CACHES = {
    'default': env.cache_url('DJANGO_CACHE')
}

##############################################################################
# Models
# https://docs.djangoproject.com/en/2.0/ref/settings/#models
##############################################################################

ABSOLUTE_URL_OVERRIDES = {}

FIXTURE_DIRS = []

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
)

LOCAL_APPS = (
    'common.apps.CommonConfig',
    'metacritic.apps.MetaCriticConfig',
    'users.apps.UsersConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

##############################################################################
# HTTP
# https://docs.djangoproject.com/en/2.0/ref/settings/#http
##############################################################################

ALLOWED_HOSTS = list(map(lambda x: x.strip(), env.list('DJANGO_ALLOWED_HOSTS')))

DEFAULT_HTTP_PROTOCOL = env.str('DJANGO_DEFAULT_HTTP_PROTOCOL')

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# https://docs.djangoproject.com/en/2.0/ref/settings/#data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

# https://docs.djangoproject.com/en/2.0/ref/settings/#data-upload-max-number-fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

DISALLOWED_USER_AGENTS = env.list('DJANGO_DISALLOWED_USER_AGENTS')

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', '10.0.2.2') if DEBUG else env.list('DJANGO_INTERNAL_IPS')

WSGI_APPLICATION = 'config.wsgi.application'

##############################################################################
# URLs
# https://docs.djangoproject.com/en/2.0/ref/settings/#urls
##############################################################################

ADMIN_URL = env.str('DJANGO_ADMIN_URL')

APPEND_SLASH = True

PREPEND_WWW = False

ROOT_URLCONF = 'config.urls'

##############################################################################
# Auth
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth
##############################################################################

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

##############################################################################
# Email
# https://docs.djangoproject.com/en/2.0/ref/settings/#email
##############################################################################

ADMINS = [tuple(admins.split(':')) for admins in env.list('DJANGO_ADMINS')]

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = env.str('DJANGO_DEFAULT_FROM_EMAIL')

SERVER_EMAIL = env.str('DJANGO_SERVER_EMAIL')

EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')

EMAIL_BACKEND = EMAIL_URL.get('EMAIL_BACKEND')

EMAIL_FILE_PATH = env.str('EMAIL_FILE_PATH', APPS_DIR.joinpath('media/email'))

EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST')

EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT')

EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = EMAIL_URL.get('EMAIL_USE_TLS')

EMAIL_USE_SSL = EMAIL_URL.get('EMAIL_USE_SSL')

EMAIL_USE_LOCALTIME = env.bool('DJANGO_EMAIL_USE_LOCALTIME')

EMAIL_SUBJECT_PREFIX = env.str('DJANGO_EMAIL_SUBJECT_PREFIX')

EMAIL_SSL_CERTFILE = env('DJANGO_EMAIL_SSL_CERTFILE')

EMAIL_SSL_KEYFILE = env('DJANGO_EMAIL_SSL_KEYFILE')

##############################################################################
# Templates
# https://docs.djangoproject.com/en/2.0/ref/settings/#id12
##############################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##############################################################################
# File uploads
# https://docs.djangoproject.com/en/2.0/ref/settings/#file-uploads
##############################################################################

DEFAULT_FILE_STORAGE = env.str('DJANGO_DEFAULT_FILE_STORAGE')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# https://docs.djangoproject.com/en/2.0/ref/settings/#file-upload-max-memory-size
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

FILE_UPLOAD_PERMISSIONS = None

FILE_UPLOAD_TEMP_DIR = None

MEDIA_ROOT = ROOT_DIR.joinpath(env.str('DJANGO_MEDIA_ROOT'))
MEDIA_URL = '/media/'

STATIC_ROOT = ROOT_DIR.joinpath(env.str('DJANGO_STATIC_ROOT'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    APPS_DIR.joinpath('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

##############################################################################
# Globalization (i18n/l10n)
# https://docs.djangoproject.com/en/2.0/ref/settings/#globalization-i18n-l10n
##############################################################################

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'N j, Y'

DATETIME_FORMAT = 'N j, Y, P'

MONTH_DAY_FORMAT = 'F j'

SHORT_DATE_FORMAT = 'm/d/Y'

SHORT_DATETIME_FORMAT = 'm/d/Y P'

TIME_FORMAT = 'P'

YEAR_MONTH_FORMAT = 'F Y'

DATE_INPUT_FORMATS = [
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y',  # '10/25/06'
    '%b %d %Y',  # 'Oct 25 2006'
    '%b %d, %Y',  # 'Oct 25, 2006'
    '%d %b %Y',  # '25 Oct 2006'
    '%d %b, %Y',  # '25 Oct, 2006'
    '%B %d %Y',  # 'October 25 2006'
    '%B %d, %Y',  # 'October 25, 2006'
    '%d %B %Y',  # '25 October 2006'
    '%d %B, %Y',  # '25 October, 2006'
]

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',  # '10/25/06 14:30'
    '%m/%d/%y',  # '10/25/06'
]

# The value must be an integer from 0 to 6, where 0 means Sunday, 1 means Monday and so on.
FIRST_DAY_OF_WEEK = 0

LANGUAGE_CODE = 'en-us'

LANGUAGES = Choices(*[(lang[0], lang[0].replace('-', '_'), lang[1]) for lang in BASE_LANGUAGES])

LOCALE_PATHS = []

##############################################################################
# Messages
# https://docs.djangoproject.com/en/2.0/ref/settings/#messages
##############################################################################

MESSAGE_LEVEL = messages.INFO

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

##############################################################################
# Debug SQL
#
##############################################################################

if env.bool('DJANGO_DEBUG_SQL'):
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'propagate': False,
        'level': 'DEBUG',
    }

if env.bool('DJANGO_DEBUG_SQL_COLOR'):
    LOGGING['handlers']['console']['formatter'] = 'sql'
    LOGGING['formatters']['sql'] = {
        '()': 'common.sqlformatter.SqlFormatter',
        'format': '%(levelname)s [%(server_time)s]\n%(message)s\n',
    }

##############################################################################
# django-rest-framework
# https://www.django-rest-framework.org
##############################################################################

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 250,
}

##############################################################################
# Project settings
#
##############################################################################

PARSER_DEFAULTS_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
}
PARSER_DEFAULT_PLATFORM = 'ps4'
PARSER_DEFAULT_PARSING_URL = 'https://www.metacritic.com/browse/games/release-date/available/{platform}/metascore?view=condensed'
PARSER_AVAILABLE_PLATFORMS = ['ps4', 'xboxone', 'switch', 'pc', 'wii-u', '3ds', 'vita', 'ios']
