# coding=utf8

import datetime
from datetime import timezone

from django.utils import timezone

DATATIME_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
DATATIME_FORMAT_YM = '%Y-%m'
DATATIME_FORMAT_YM_NO_SEP = '%Y%m'
DATATIME_FORMAT_YMD = '%Y-%m-%d'
DATATIME_FORMAT_YMD_NO_SEP = '%Y%m%d'
DATATIME_FORMAT_YMD_EN = '%d/%m/%Y'
DATATIME_FORMAT_HM = '%H:%M'
DATATIME_FORMAT_HMS = '%H:%M:%S'


def get_cur_datetime():
    """
    datetime.datetime
    @return:
    """
    from django.utils import timezone
    return timezone.localtime(timezone.now())


def get_day_datetime_full():
    """
    获取今天日期时间（包括时分秒）
    @return:
    """

    return get_cur_datetime().strftime(DATATIME_FORMAT_FULL)


def get_current_timestamp(is_to_int=True, is_millisecond=False):
    """
    当前时间戳
    @param is_to_int: 是否转成int，默认 True是
    @param is_millisecond: 是否要转成毫秒
    @return:
    """
    current_timestamp = int(get_cur_datetime().timestamp())
    if is_to_int:
        if is_millisecond:
            return int(current_timestamp * 1000)
        else:
            return int(current_timestamp)
    return current_timestamp


def datetime_format_to_str(date_time, fmt=DATATIME_FORMAT_FULL):
    """
    日期对象转换为字符串
    :param date_time:
    :param fmt:
    :return:
    """
    if not isinstance(date_time, datetime.datetime):
        return False

    # UTC 转为当前时区
    try:
        timezone_datetime = timezone.localtime(date_time)
    except Exception:
        date_time = timezone.make_aware(date_time, timezone.get_default_timezone())
        timezone_datetime = timezone.localtime(date_time)

    return timezone_datetime.strftime(fmt)


def datetime_is_today(source_datetime):
    """
    datetime 是不是今天
    @param source_datetime:
    @return:
    """
    if not isinstance(source_datetime, datetime.datetime):
        return False

    # UTC 转为当前时区
    timezone_datetime = timezone.localtime(source_datetime)

    return timezone_datetime.date() == get_cur_datetime().date()


def datetime_is_yesterday(source_datetime):
    """
    datetime 是不是昨天
    @param source_datetime:
    @return:
    """
    if not isinstance(source_datetime, datetime.datetime):
        return False

    # UTC 转为当前时区
    timezone_datetime = timezone.localtime(source_datetime)

    return timezone_datetime.date() == (get_cur_datetime() - datetime.timedelta(days=1)).date()


def datetime_is_tomorrow(source_datetime):
    """
    datetime 是不是明天
    @param source_datetime:
    @return:
    """
    if not isinstance(source_datetime, datetime.datetime):
        return False

    # UTC 转为当前时区
    timezone_datetime = timezone.localtime(source_datetime)

    return timezone_datetime.date() == (get_cur_datetime() + datetime.timedelta(days=1)).date()
