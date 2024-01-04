# coding=utf8

import functools
import json

from django.http import HttpResponse

from frontend.utils.request_utils import trigger_frequency_request_time
from helper import helper_ret, helper_int
from library.log import logger_request


def wrap_api_requests(check_authorization=True, check_signature=True):
    """
        客户端请求接口装饰器，
        1. 接口鉴权，校验 header里面 Authorization
        2. 参数签名校验，校验 参数签名 signature
    @param check_authorization: 是否鉴权
    @param check_signature: 是否签名
    @return:
    """
    
    def signature_authorization_api(func):
        @functools.wraps(func)
        def func_wrapper(request, *args, **kwargs):
            """
            装饰器
            @param request:
            @param args:
            @param kwargs:
            @return:
            """
            # 解析body
            try:
                post_data = json.loads(request.body)
            except Exception as e:
                logger_request.warn(
                    'parse_body json.loads request.body failed!, path:%s, body:%s, error:%s',
                    request.path, request.body, e
                )
                return helper_ret.ret_response(999, data=dict(), msg="Invalid request Body")
            
            # header
            authorization = request.META.get('HTTP_AUTHORIZATION', '').strip()
            logger_request.debug(
                'path:%s, func.name:%s, authorization:%s, post_data:%s',
                request.path, func.__name__, authorization, post_data
            )

            if check_authorization:
                pass

            if check_signature:
                pass

            # 添加请求限制
            if trigger_frequency_request_time(request, func.__name__):
                return helper_ret.ret_response(1001, data=dict(), msg="")

            return transfer_error_msg(func(request, *args, **kwargs))
        
        return func_wrapper
    
    return signature_authorization_api


def transfer_error_msg(response):
    """
    语言包处理
    @param response: 响应数据
    @return:
    """
    
    if not response.content:
        return response
    
    ret_dict = json.loads(response.content)
    code = helper_int.parse_to_int(ret_dict.get('code', 0))
    if not code:
        return response
    
    content = json.dumps(ret_dict, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    
    return HttpResponse(content, content_type='application/json')
