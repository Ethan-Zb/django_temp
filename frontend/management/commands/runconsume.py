# coding=utf8

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'run consume'
    
    def add_arguments(self, parser):
        """
        增加命令运行参数
        @param parser:
        @return:
        """
        parser.add_argument('max_workers')
    
    def handle(self, *args, **options):
        """
        脚本
        python manage.py runconsume 3
        @param args:
        @param options:
        @return:
        """
        pass
