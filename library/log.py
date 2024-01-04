# coding=utf8

import logging

# 公共log
logger = logging.getLogger('main')

# django
logger_django = logging.getLogger('django')

# http 请求
logger_request = logging.getLogger('request')

# celery
logger_celery = logging.getLogger('xcelery')

# sql
logger_mysql = logging.getLogger('x_mysql')

# time_cost
logger_time = logging.getLogger('consuming')