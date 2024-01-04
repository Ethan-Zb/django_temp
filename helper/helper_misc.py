# coding=utf8

import socket
import struct

from library.log import logger


def ip_to_int(ip):
    """
    IP地址转int
    `struct.unpack("!I", socket.inet_aton(ip))[0]` 会将 IP 地址字符串转换为无符号整数 (unsigned int) 类型。具体来说，这段代码执行以下步骤：

    1. `socket.inet_aton(ip)` 将 IP 地址字符串 `ip` 转换为 32 位二进制表示的网络字节顺序的值。
    2. `struct.unpack("!I", ...)` 使用 `struct` 模块将这个二进制值解包成一个无符号整数 (unsigned int)，`!I` 表示网络字节顺序 (big-endian) 的无符号整数。
    3. 最后，`[0]` 从解包的结果中取出第一个元素，即无符号整数值。
    所以，最终的结果是一个无符号整数，它表示了给定 IP 地址的数值形式。这个整数不会有符号，因为它代表一个 IP 地址，而 IP 地址不是有符号的整数。如果你要确保结果是正数，你可以使用 `abs()` 函数来获取它的绝对值。
    :param ip:
    :return:
    """
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))


def get_client_ip_from_request(request):
    """
    获取请求者的IP信息
    X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP代理或者负载均衡服务器时才会添加该项。
    @param request:
    @return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    
    if not ip:
        ip = request.META.get('HTTP_X_REAL_IP')
    
    return "0.0.0.1" if not ip else ip


def close_invalid_db_conns():
    """
    支持断线重连
    """
    from django.db import connections
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def recycle_invalid_db_conns(func):
    """
       回收 Django无效的数据库连接
    """
    
    def func_wrapper(*args, **kwargs):
        close_invalid_db_conns()
        result = func(*args, **kwargs)
        close_invalid_db_conns()
        
        return result
    
    return func_wrapper


def celery_func_delay(func, *args, **kwargs):
    """
    celery delay调用
    delay接收的参数会全部传递到任务函数
    ex:
        test.delay('a', 'b', kwarg1='x', kwarg2='y')
        test.apply_async(args=['a', 'b'], kargs={'kwarg1': 'x', 'kwarg2': 'y'})
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        return func.delay(*args, **kwargs)
    except Exception as e:
        logger.fatal('exc occur. e: \n%s\nfunc: \n%s', e, func, exc_info=True)
        return e


def celery_func_apply_async(func, countdown, *args, **kwargs):
    """
    celery apply_sync 异步调用
    apply_sync 接收的参数只有args和 kwargs会传递给任务函数
    ex:
        celery_func_apply_async(func, countdown=1, a=1, b=2, c=3)
    @param func:
    @param countdown:  接收一个数字或浮点数，任务将在countdown秒后执行
    @param args:
    @param kwargs:
    @return:
    """
    try:
        return func.apply_async(args, kwargs, countdown=countdown)
    except Exception as e:
        logger.fatal('exc occur. e: \n%s\nfunc: \n%s', e, func, exc_info=True)
        return e


def dict_fetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    @param cursor:
    @return:
    """
    if not cursor:
        return []
    
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
