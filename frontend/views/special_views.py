# coding=utf8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe

from helper import (helper_ret)


def page_not_found(request):
    """
    401
    @param request:
    @return:
    """
    return HttpResponse('Unauthorized', status=401)


@require_safe
@csrf_exempt
def health_check(request):
    """
    健康检查
    @param request:
    @return:
    """
    return helper_ret.ret_response(data=dict(status='online'))
