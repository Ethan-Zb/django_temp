# coding=utf8

from config import redis_config
from library.bloom import BloomFilter
from library.redis import LibRedis

# 默认redis
redis_default = LibRedis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    db=redis_config.REDIS_DB
)

# 布隆过滤器
redis_bloom = LibRedis(
    host=redis_config.REDIS_BLOOM_HOST,
    port=redis_config.REDIS_BLOOM_PORT,
    db=redis_config.REDIS_BLOOM_DB,
    expired=60 * 60 * 24 * 15
)

# 短时间内临时缓存，如用于限制请求频率
redis_frequent = LibRedis(
    host=redis_config.REDIS_FREQUENT_HOST,
    port=redis_config.REDIS_FREQUENT_PORT,
    db=redis_config.REDIS_FREQUENT_DB,
    expired=60,
)