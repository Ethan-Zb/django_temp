# coding=utf8

"""
Django 4.1.7
"""
import os
from pathlib import Path

import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r3(uk6r2vgu-k2w0hhb3mirv)n_w*9hz25x8&oloagl1rbfo3s'
DEBUG = config.DEBUG

ALLOWED_HOSTS = ['*', ]
CSRF_TRUSTED_ORIGINS = config.CSRF_TRUSTED_HOST
CORS_ORIGIN_ALLOW_ALL = 'ALL'
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# 20Mb
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend.apps.FrontendConfig',
    "db_master.apps.DbMasterConfig",
    "db_user.apps.DbUserConfig",
    "db_news.apps.DbNewsConfig",
    "celerytasks",
]

MIDDLEWARE = [
    'middlewares.time_consuming.TimeConsumingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.catch_exception.CatchExceptionMiddleware',
]

ROOT_URLCONF = 'django_temp.urls'

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

WSGI_APPLICATION = 'django_temp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.MYSQL_DATABASE,
        'USER': config.MYSQL_USER,
        'PASSWORD': config.MYSQL_PASSWORD,
        'HOST': config.MYSQL_HOST,
        'PORT': config.MYSQL_PORT,
        'CONN_MAX_AGE': config.MYSQL_CONN_MAX_AGE,
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'db_user': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.MYSQL_USER_DATABASE,
        'USER': config.MYSQL_USER_USER,
        'PASSWORD': config.MYSQL_USER_PASSWORD,
        'HOST': config.MYSQL_USER_HOST,
        'PORT': config.MYSQL_USER_PORT,
        'CONN_MAX_AGE': config.MYSQL_USER_CONN_MAX_AGE,
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'db_news': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.MYSQL_NEWS_DATABASE,
        'USER': config.MYSQL_NEWS_USER,
        'PASSWORD': config.MYSQL_NEWS_PASSWORD,
        'HOST': config.MYSQL_NEWS_HOST,
        'PORT': config.MYSQL_NEWS_PORT,
        'CONN_MAX_AGE': config.MYSQL_NEWS_CONN_MAX_AGE,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = config.LANGUAGE_CODE

TIME_ZONE = config.TIME_ZONE

USE_I18N = True

USE_TZ = config.USE_TZ

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAIN_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/main.log")
DJANGO_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/django.log")
REQUEST_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/request.log")
CELERY_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/celery.log")
TIMECOST_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/consuming.log")
MYSQL_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/mysql.log")

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(module)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

MAIN_LOG_LEVEL = config.MAIN_LOG_LEVEL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
            'encoding': 'utf8',
        },
    },
    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda x: DEBUG,
        }
    },
    'handlers': {
        'send_warning': {
            'level': 'ERROR',
            'class': 'library.handlers.LogWarningHandler',
        },
        'django_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DJANGO_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'main_file': {
            'level': MAIN_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'request_file': {
            'level': MAIN_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': REQUEST_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'celery_file': {
            'level': MAIN_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CELERY_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'time_cost_file': {
            'level': MAIN_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': TIMECOST_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'mysql_file': {
            'level': MAIN_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MYSQL_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 1024 * 3,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
        'django.request': {
            'handlers': ['django_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': True,
        },
        'main': {
            'handlers': ['main_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
        'request': {
            'handlers': ['request_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
        'xcelery': {
            'handlers': ['celery_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
        'consuming': {
            'handlers': ['time_cost_file'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
        'x_mysql': {
            'handlers': ['mysql_file', 'send_warning'],
            'level': MAIN_LOG_LEVEL,
            'propagate': False
        },
    }
}

# 数据库路由
DATABASE_ROUTERS = [
    'db_router.RouterDatabaseDefault',
    'db_router.RouterDatabaseUser',
    'db_router.RouterDatabaseNews',
]
