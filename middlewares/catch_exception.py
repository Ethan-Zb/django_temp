# coding=utf8
"""
异常捕获中间件
"""
from django.middleware.common import MiddlewareMixin

from config.error.error_code import ERROR_5005_INTERNAL_SERVER_ERROR
from helper import helper_ret
from library.log import logger_django


class CatchExceptionMiddleware(MiddlewareMixin):
    """
    捕获异常
    """
    
    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        self.sync_capable = True

        import traceback
        logger_django.fatal(
            'middleware process_exception, path:%s, body:%s, error:%s, exc:%s',
            request.path, request.body, exception, traceback.format_exc()
        )
        
        return helper_ret.ret_response(
            ERROR_5005_INTERNAL_SERVER_ERROR,
            data=dict(),
            msg=""
        )
