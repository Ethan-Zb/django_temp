# coding=utf8

import os

from django.contrib.gis.geoip2 import GeoIP2Exception, GeoIP2

from config import GEOIP_PATH
from library.log import logger


class LibGeoIp(object):

    def __init__(self):
        if not os.path.isfile(GEOIP_PATH):
            logger.error("LibGeoip GEOIP_PATH not exists, GEOIP_PATH:%s", GEOIP_PATH)
            raise GeoIP2Exception

        self.geo = GeoIP2(path=GEOIP_PATH)

    def get_ip_by_country(self, my_ip=''):
        """
        根据IP查询国家
        默认返回：pt
        @param self:
        @param my_ip:
        @return:
        """
        my_country_name = self.geo.country_name(my_ip)
        return my_country_name
