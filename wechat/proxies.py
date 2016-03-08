# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from .models import Proxy

class MysqlProxyBackend(object):
    def __init__(self):
        proxy = Proxy.objects.filter(status=Proxy.STATUS_SUCCESS).order_by('?').first()
        if proxy:
            self.user = proxy.user
            self.password = proxy.password
            self.host = proxy.host
            self.port = proxy.port
        else:
            self.user, self.password, self.host, self.port = '', '', '', ''

    def __str__(self):
        return ':'.join([str(self.user), str(self.password), str(self.host), str(self.port)])
