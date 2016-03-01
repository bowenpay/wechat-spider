# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import redis
import json
from django.conf import settings
from hashlib import md5
REDIS_POOL = None


def get_redis_pool():
    global REDIS_POOL
    if not REDIS_POOL:
        REDIS_POOL = redis.ConnectionPool(**settings.REDIS_OPTIONS)

    return REDIS_POOL


def get_redis():
    return redis.Redis(connection_pool=get_redis_pool())


def get_uniqueid(url):
    link = get_link_from_url(url)
    return md5(link).hexdigest()


def get_link_from_url(url):
    if isinstance(url, basestring):
        return url
    elif isinstance(url, dict):
        return json.dumps(url)