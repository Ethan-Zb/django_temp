# coding=utf8

from config import env

HOST = '127.0.0.1'

# 默认redis
REDIS_HOST = env.dict('REDIS_DEFAULT', default={}).get('host', HOST)
REDIS_PORT = int(env.dict('REDIS_DEFAULT', default={}).get('port', 6379))
REDIS_DB = int(env.dict('REDIS_DEFAULT', default={}).get('db', 0))

# celery redis
REDIS_CELERY_HOST = env.dict('REDIS_CELERY', default={}).get('host', HOST)
REDIS_CELERY_PORT = int(env.dict('REDIS_CELERY', default={}).get('port', 6379))
REDIS_CELERY_DB = int(env.dict('REDIS_CELERY', default={}).get('db', 1))

# Bloomfilter
REDIS_BLOOM_HOST = env.dict('REDIS_BLOOM', default={}).get('host', HOST)
REDIS_BLOOM_PORT = int(env.dict('REDIS_BLOOM', default={}).get('port', 6379))
REDIS_BLOOM_DB = int(env.dict('REDIS_BLOOM', default={}).get('db', 2))

# redis frequent 限制请求频率
REDIS_FREQUENT_HOST = env.dict('REDIS_FREQUENT', default={}).get('host', HOST)
REDIS_FREQUENT_PORT = int(env.dict('REDIS_FREQUENT', default={}).get('port', 6379))
REDIS_FREQUENT_DB = int(env.dict('REDIS_FREQUENT', default={}).get('db', 3))
