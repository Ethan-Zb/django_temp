# coding=utf8
import logging
from logging import Handler

import requests

from helper import helper_int
from library.log import logger


class LogWarningHandler(Handler):
    """
    log warning handler
    """

    app_token = ""
    post_url = ""

    message_common = """
    【日志名】: {name}
    【日志级别】: {levelname}
    【时间】: {asctime}
    【进程ID】: {process}
    【线程ID】: {thread}
    【文件】: {filename}
    【函数】: {funcname}
    【代码行】: {lineno}
    【信息】: {message}
    """

    def __init__(self):
        Handler.__init__(self)

    def emit(self, record):
        """
        重写emit方法
        @param record:
        @return:
        """
        try:
            # 需要 ERROR 级别
            if record.levelno < logging.ERROR:
                return

            message = self.message_common
            message = message.format(
                name=record.name,
                levelname=record.levelname,
                asctime=record.asctime,
                process=record.process,
                thread=record.thread,
                filename=record.pathname,
                funcname=record.funcName,
                lineno=record.lineno,
                message=record.getMessage(),
            )

            # 发送消息
            self.send_message(message)

        except Exception as e:
            logger.warn("LogWarningHandler emit record error, error:%s", e)

    def send_message(self, message):
        """
        发送消息
        @return:
        """
        data_dict = {"message": message}
        token = self.app_token
        if not token:
            logger.warn("LogWarningHandler send_message error, not found token, data_dict:%s", data_dict)
            return
        headers = {
            "content-type": "application/json; charset=UTF-8",
            'Authorization': '{}'.format(token)
        }
        # 发送消息
        rsp = requests.post(url=self.post_url, json=data_dict, headers=headers, timeout=3)
        rsp_dict = rsp.json()
        if not rsp or not rsp_dict or not isinstance(rsp_dict, dict):
            return

        if helper_int.parse_to_int(rsp_dict.get('code', -1)) > 0:
            logger.warn("LogWarningHandler send_message error, rsp dict:%s", rsp_dict)
            return

        return
