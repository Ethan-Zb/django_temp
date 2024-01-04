# coding=utf8

from db_router.base_router import MysqlRouterBase


class RouterDatabaseDefault(MysqlRouterBase):
    """
    default
    """
    DB_NAME = 'default'
    APP_NAME = 'db_master'


class RouterDatabaseUser(MysqlRouterBase):
    """
    user
    """
    DB_NAME = 'db_user'
    APP_NAME = 'db_user'


class RouterDatabaseNews(MysqlRouterBase):
    """
    news
    """
    DB_NAME = 'db_news'
    APP_NAME = 'db_news'
