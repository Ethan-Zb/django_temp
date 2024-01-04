# coding=utf8
"""
限制请求频率
"""

from helper.helper_misc import get_client_ip_from_request
from library import redis_frequent


def trigger_frequency_request_time(request, func_name):
    """
    是否触发
    限制请求频率, 通过设备码, 没有的话限制ip
    @param request:
    @param func_name:
    @return: true-触发频控
    """
    # 过滤掉不需要频率限制的接口
    filter_func_list = [
        "health_check",
    ]
    if func_name in filter_func_list:
        return False

    ip = get_client_ip_from_request(request)
    key = f"frequent_{func_name}_{ip}"
    # SET if Not exists
    if not redis_frequent.set_nx(key, 1):
        # 设置过期时间
        redis_frequent.set_p_expire(key, 800)
        return True
    
    # 设置过期时间
    redis_frequent.set_p_expire(key, 800)
    return False
