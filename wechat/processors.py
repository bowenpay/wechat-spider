# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from wechatspider.util import get_uniqueid


class DjangoModelBackend(object):
    def __init__(self, _class):
        self._class = _class

    def process(self, params):
        C = self._class
        params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))
        C.objects.update_or_create(uniqueid=params['uniqueid'], defaults=params)

