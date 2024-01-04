# coding=utf8

import os

import environ

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# conf，json 等文件目录
CONFIGURE_DIR = os.path.join(BASE_DIR, 'configure')

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.app_env_setting'), recurse=False, override=True)

ENV_DEV = 'DEV'
ENV_TEST = 'TEST'
ENV_PROD = 'PROD'

APP_ENV = env.str('ENV', ENV_DEV)

DEBUG = env.bool('DEBUG', True)
MAIN_LOG_LEVEL = env.str('MAIN_LOG_LEVEL', 'DEBUG')

WEB_HOST = env.str('WEB_HOST', 'http://127.0.0.1')
STATIC_HOST = env.str('STATIC_HOST', 'http://127.0.0.1')
MEDIA_HOST = env.str('MEDIA_HOST', 'http://127.0.0.1')

MYSQL_HOST = env.str('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = env.int('MYSQL_PORT', 3306)
MYSQL_DATABASE = env.str('MYSQL_DATABASE', '')
MYSQL_USER = env.str('MYSQL_USER', '')
MYSQL_PASSWORD = env.str('MYSQL_PASSWORD', '')
MYSQL_CONN_MAX_AGE = env.int('MYSQL_CONN_MAX_AGE', 28800)

MYSQL_NEWS_HOST = env.str('MYSQL_NEWS_HOST', '127.0.0.1')
MYSQL_NEWS_PORT = env.int('MYSQL_NEWS_PORT', 3306)
MYSQL_NEWS_DATABASE = env.str('MYSQL_NEWS_DATABASE', '')
MYSQL_NEWS_USER = env.str('MYSQL_NEWS_USER', '')
MYSQL_NEWS_PASSWORD = env.str('MYSQL_NEWS_PASSWORD', '')
MYSQL_NEWS_CONN_MAX_AGE = env.int('MYSQL_NEWS_CONN_MAX_AGE', 28800)

MYSQL_USER_HOST = env.str('MYSQL_USER_HOST', '127.0.0.1')
MYSQL_USER_PORT = env.int('MYSQL_USER_PORT', 3306)
MYSQL_USER_DATABASE = env.str('MYSQL_USER_DATABASE', '')
MYSQL_USER_USER = env.str('MYSQL_USER_USER', '')
MYSQL_USER_PASSWORD = env.str('MYSQL_USER_PASSWORD', '')
MYSQL_USER_CONN_MAX_AGE = env.int('MYSQL_USER_CONN_MAX_AGE', 28800)

LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'zh-Hans')
TIME_ZONE = env.str('TIME_ZONE', 'Asia/Shanghai')
USE_TZ = env.bool('USE_TZ', True)
CSRF_TRUSTED_HOST = env.list('CSRF_TRUSTED_HOST', [])
GEOIP_PATH = env.str('GEO_PATH', os.path.join(CONFIGURE_DIR, 'GeoLite2-Country.mmdb'))
