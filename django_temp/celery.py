# coding=utf-8
"""
celery
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_temp.settings')

from celery import Celery
from celery.loaders.app import AppLoader


class CeleryAppLoader(AppLoader):
    """
    "Default loader used when an app is specified.
    """
    
    def on_worker_init(self):
        """
        Called when the worker (:program:`celery worker`) starts.
        @return:
        """
        pass


def init_celery_app():
    """
    celery 实例化
    @return:
    """
    
    from celerytasks.apps import CeleryTasksConfig
    celery_app = Celery(loader='django_temp.celery.CeleryAppLoader')
    celery_app.conf.update(CeleryTasksConfig.celery_conf)
    celery_app.autodiscover_tasks(packages=['celerytasks'])
    celery_app.autodiscover_tasks(packages=['celerytasks'], related_name='signal_tasks')

    return celery_app


app_celery = init_celery_app()
