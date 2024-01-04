# coding=utf8

from celery import shared_task


@shared_task
def test():
    print("Hello Ethan")
