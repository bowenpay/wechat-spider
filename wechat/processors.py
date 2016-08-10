# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from wechatspider.util import get_uniqueid
from wechat.constants import KIND_DETAIL, KIND_KEYWORD
from wechat.models import Wechat

class DjangoModelBackend(object):
    def __init__(self, _class):
        self._class = _class

    def process(self, params):
        C = self._class
        # 排除被屏蔽的情况
        if 'mp.weixin.qq.com' not in params.get('url'):
            return
        # 排除代理失败的情况
        if 'wx.qq.com' not in params.get('source'):
            return
        # 存储数据
        if params.get('kind') in [KIND_DETAIL, KIND_KEYWORD]:
            params.pop('kind', None)
            params.pop('retry', None)
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
                "status": Wechat.STATUS_DISABLE
            })
            # 如果微信号状态为已删除,则不保存这篇文章
            if wechat.status == Wechat.STATUS_DELETE:
                return

            # 保存文章
            params['wechat_id'] = wechat.id
            params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))
            C.objects.update_or_create(uniqueid=params['uniqueid'], defaults=params)

        else:
            params.pop('kind', None)
            params.pop('retry', None)
            params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))
            C.objects.update_or_create(uniqueid=params['uniqueid'], defaults=params)

