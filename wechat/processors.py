# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from wechatspider.util import get_uniqueid
from wechat.constants import KIND_DETAIL
from wechat.models import Wechat

class DjangoModelBackend(object):
    def __init__(self, _class):
        self._class = _class

    def process(self, params):
        C = self._class
        if params.get('kind') == KIND_DETAIL:
            params.pop('kind', None)
            # 保存微信号
            wechatid = params.pop('wechatid', '')
            name = params.pop('name', '')
            intro = params.pop('intro', '')
            qrcode = params.pop('qrcode', '')
            wechat, created = Wechat.objects.get_or_create(wechatid=wechatid, defaults={
                "wechatid": wechatid,
                "name": name,
                "intro": intro,
                "qrcode": qrcode,
            })
            # 保存文章
            params['wechat_id'] = wechat.id
            params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))
            C.objects.update_or_create(uniqueid=params['uniqueid'], defaults=params)

        else:
            params.pop('kind', None)
            params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))
            C.objects.update_or_create(uniqueid=params['uniqueid'], defaults=params)

