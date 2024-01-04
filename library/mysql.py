# coding=utf8
"""
mysql 辅助函数
"""
from django.db import connections
from django_temp.settings import DATABASES
from library.log import logger_mysql
from helper.helper_string import to_string


def check_ret_database(database):
    """
    检查数据库 是否有效, 有效则返回 database，无效则返回false
    @param database:
    @return:
    """
    if not database:
        logger_mysql.error('check_ret_database failed!, database:%s', database)
        return False
    
    database = to_string(database)
    if database in DATABASES:
        return database
    
    logger_mysql.error('check_ret_database failed, not in setting, database:%s', database)
    return False


def dict_fetchall(cursor):
    """
    Return all rows from a cursor as a dict
    @param cursor:
    @return:
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def query(database, sql):
    """
    执行原生sql语句
    ex: mysql.query('default / db_user / db_news', sql), boolean
    @param database:
    @param sql:
    @return:
    """
    database = check_ret_database(database)
    if not database:
        return False
    
    cursor = connections[database].cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        logger_mysql.error('query failed!, database:%s, sql:%s, e:%s', database, sql, e)
        return False
    
    cursor.close()
    return True


def fetch_one(database, sql):
    """
    查询数据， 只取第一条
    ex: mysql.fetch_one('default', sql),  dict()
    @param database:
    @param sql:
    @return:
    """
    database = check_ret_database(database)
    if not database:
        return dict()
    
    cursor = connections[database].cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        cursor.close()
        logger_mysql.error('fetch_one from mysql failed!,sql:%s, e:%s', sql, e)
        return dict()
    
    record_dict = dict_fetchall(cursor)
    cursor.close()
    if not record_dict:
        return dict()
    
    return record_dict[0]


def fetch_all(database, sql):
    """
    查询数据, 取所有记录
    ex: mysql.fetch_all('default', sql), dict()
    @param database:
    @param sql:
    @return:
    """
    database = check_ret_database(database)
    if not database:
        return dict()
    
    cursor = connections[database].cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        cursor.close()
        logger_mysql.error('fetch_all from mysql failed!,sql:%s, e:%s', sql, e)
        return dict()
    
    record_dict = dict_fetchall(cursor)
    cursor.close()
    if not record_dict:
        return dict()
    
    return record_dict
