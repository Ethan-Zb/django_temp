# coding=utf8

from celery.schedules import crontab
from django.apps import AppConfig

from config import redis_config, TIME_ZONE


class CeleryTasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celerytasks'
    
    celery_conf = dict(
        broker_url='redis://{host}:{port}/{db}'.format(
            host=redis_config.REDIS_CELERY_HOST,
            port=redis_config.REDIS_CELERY_PORT,
            db=redis_config.REDIS_CELERY_DB
        ),
        enable_utc=False,
        timezone=TIME_ZONE,
        task_default_queue='default',
        broker_connection_retry_on_startup=False,
        task_publish_retry_policy={
            'max_retries': 3,      # 放弃之前的最大重试次数， 默认为3
            'interval_start': 0,   # 定义两次重试之间要等待的秒数（浮点数或整数）。默认值为0（第一次重试将立即执行）。
            'interval_step': 0.2,  # 在每次连续重试时，此数字将被添加到重试延迟中（浮点数或整数）。默认值为0.2。
            'interval_max': 0.2,   # 重试之间等待的最大秒数（浮点数或整数）。默认值为0.2
        },
        # 路由器列表，默认值为0
        task_routes={
            'celerytasks.tasks.*': {
                'queue': 'default'
            },
            'celerytasks.signal_tasks.*': {
                'queue': 'default'
            },

        },
        beat_schedule={
            'test': {
                'task': 'celerytasks.tasks.test',
                'schedule': crontab(minute='0', hour='0'),
            },
        },
    )
