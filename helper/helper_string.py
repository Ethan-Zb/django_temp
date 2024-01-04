# coding=utf8
import re
import string
from decimal import Decimal


def to_string(s_str):
    """
    转字符串
    @param s_str:
    @return:
    """
    if not s_str:
        return ""

    if isinstance(s_str, Decimal):
        return str(s_str)

    if not isinstance(s_str, (str, int, bytes)):
        return ""

    if isinstance(s_str, bytes):
        return s_str.decode('utf-8').strip()

    if isinstance(s_str, int):
        return str(s_str).strip()

    return s_str.strip()


def to_bytes(s_str):
    """
    转bytes
    @param s_str:
    @return:
    """
    if not isinstance(s_str, (str, int, bytes)):
        return None

    if isinstance(s_str, str):
        return s_str.encode('utf-8')

    if isinstance(s_str, int):
        return str(s_str).encode('utf-8')

    return s_str


def generate_md5_str(src_str):
    """
    字符串生成md5
    @param src_str:
    @return:
    """
    import hashlib
    src_str = to_string(src_str)
    return hashlib.md5(src_str.encode('utf-8')).hexdigest()


def generate_base64_str(src_str, extra_content=None):
    """
    base64加密
    :param src_str:加密内容
    :param extra_content:特殊位：添加到末尾
    :return:
    """
    import base64
    src_str = to_string(src_str)
    if extra_content:
        src_str += extra_content
    encoded_data = base64.b64encode(src_str.encode('utf-8')).decode('utf-8')
    return encoded_data


def generate_random_str(length=8):
    """
    生成随机字符串
    @param length: 字符串长度
    @return:
    """
    from django.utils.crypto import get_random_string
    from helper import helper_int

    length = helper_int.parse_to_int(length)
    if not length:
        length = 8

    return get_random_string(length)


def is_container_chinese(some_str):
    """
    字符串是否包含中文
    @param some_str:
    @return:
    """
    some_str = to_string(some_str)
    if not some_str:
        return False

    return re.compile(u'[\u4e00-\u9fa5]').search(some_str)


def trim_ai_string(str_txt):
    """
    strip ai 字符串
    @param str_txt:
    @return:
    """
    str_txt = to_string(str_txt)
    if not str_txt:
        return ""

    for i in string.punctuation:
        str_txt = str_txt.replace(i, '')

    return str_txt.strip()
