# coding=utf8
"""
计算接口cost时间
"""
import json

from django.middleware.common import MiddlewareMixin

from helper import helper_time
from library.log import logger_time


class TimeConsumingMiddleware(MiddlewareMixin):
    """
    接口耗时
    """
    
    def process_request(self, request):
        """
        请求
        @param request: 请求对象
        @return:
        """
        request.start_milli_time = helper_time.get_current_timestamp(is_millisecond=True)
    
    def process_response(self, request, response):
        """
        响应
        @param request:
        @param response:
        @return:
        """
        if not hasattr(request, 'start_milli_time'):
            return response
        
        time_cost = helper_time.get_current_timestamp(is_millisecond=True) - request.start_milli_time
        path = request.get_full_path()
        
        ret_dict = dict()
        message = ""
        if hasattr(response, 'content'):
            try:
                ret_dict = json.loads(response.content)
            except Exception as e:
                message = response.content
        
        logger_time.error(
            "path:%s,  time_cost:%s, response code:%s, message:%s",
            path, time_cost, ret_dict.get('code', -123), message
        )
        
        return response
