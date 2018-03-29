"""
Django settings for cityback project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import ast

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'e(l(earh23inam!br%-dd%@c5z(_esulairx35nkmx4f(9h(i5')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))


ALLOWED_HOSTS = ast.literal_eval(os.environ.get('DJANGO_HOST', "[]"))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_nose',
    'cityback.storage',
    'cityback.processing',
    'cityback.retrieval',
    'channels',
    'cityback.dashboard',
    'cityback.visualisation'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cityback.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cityback.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

db_user = os.environ.get('PGUSER1', "")
db_password = os.environ.get('PGPASSWORD', "")
db_name = os.environ.get('PGDB', "")
db_host = os.environ.get('PGHOST', "127.0.0.1")
if db_user == "":
    raise ValueError("PGUSER1 not defined, did you import settings?")

if db_user != "" and db_password != "" and db_name != "":
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

redis_host = os.environ.get('REDIS_HOST', "127.0.0.1")
redis_password = os.environ.get('REDIS_PASSWORD', '')
if redis_password != '':
    redis_host = ":" + redis_password + "@" + redis_host

redis_url = 'redis://' + redis_host + ':6379/0'
celery_url = os.environ.get('CELERY_URL', redis_url)
CELERY_BROKER_URL = celery_url
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': 'eu-west-1',
                                   'visibility_timeout': 43200}

# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'


#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
# CELERY_TASK_SERIALIZER = 'json'

# Channel layer settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [redis_url],
        },
    },
}

ASGI_APPLICATION = "cityback.routing.application"

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=cityback.storage,cityback.retrieval,'
    'cityback.dashboard,'
    'cityback.visualisation,'
    'cityback.scheduler,'
    'cityback.processing',
    '--cover-html'
]
