# coding=utf8

from library.log import logger


def parse_to_int(mixed):
    """
    parse_to_int 转int
    @param mixed: int or str
    @return:
    """
    import decimal
    
    if mixed is None:
        return 0
    
    if isinstance(mixed, (float, decimal.Decimal,)):
        return int(mixed)
    
    if isinstance(mixed, int):
        return int(mixed)
    
    try:
        if isinstance(mixed, tuple):
            if len(mixed) == 1 and isinstance(mixed[0], (int, float, decimal.Decimal, str, bytes)):
                return int(mixed[0])
        
        if not isinstance(mixed, (str, bytes)):
            return 0
        
        if mixed.isdigit() or mixed.lstrip('-').isdigit() or mixed.lstrip('+').isdigit():
            return int(mixed)
    except Exception as e:
        logger.warn("parse_to_int except e:%s", e)
        return 0
    
    return 0


def userid_to_int(user_id):
    """
    user_id转int
    @param user_id: 用户uid
    @return:
    """
    if not user_id:
        return 0
    
    _uid = parse_to_int(user_id)
    if not _uid:
        return 0
    
    return max(0, _uid)
