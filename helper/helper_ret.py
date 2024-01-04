# coding=utf8

import json

from django.http import HttpResponse

from helper import helper_time


def ret_response(code=0, data=None, msg="ok"):
    """
    响应返回
    @param code: 错误码， 0-成功，非0失败
    @param data: 非0， 字符串，0=json
    @param msg:
    @return:
    """
    response = dict(
        code=code,
        data=data if data is not None else dict(),
        msg=msg.strip(),
        time=helper_time.get_current_timestamp(),
    )
    content = json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return HttpResponse(content, content_type='application/json')
