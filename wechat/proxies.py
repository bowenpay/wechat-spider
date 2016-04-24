# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.db import transaction
from .models import Proxy

class MysqlProxyBackend(object):
    def __init__(self):
        # 手动commit, 确保获取最新的数据
        transaction.enter_transaction_management()
        transaction.commit()
        proxy = Proxy.objects.filter(kind=Proxy.KIND_DOWNLOAD, status=Proxy.STATUS_SUCCESS).order_by('?').first()
        if proxy:
            self.user = proxy.user
            self.password = proxy.password
            self.host = proxy.host
            self.port = proxy.port
        else:
            self.user, self.password, self.host, self.port = '', '', '', ''

    def is_valid(self):
        return self.host and self.port

    def __str__(self):
        return ':'.join([str(self.user), str(self.password), str(self.host), str(self.port)])
