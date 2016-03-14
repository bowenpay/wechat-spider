# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
from django.core.management.base import BaseCommand
from wechat.models import Proxy
from wechat.util import check_proxy
import requests
import logging
logger = logging.getLogger()

class Command(BaseCommand):
    help = 'get proxies'

    def handle(self, *args, **options):
        while True:
            time.sleep(5)
            self.get_proxies()

    def get_proxies(self):
        # 快代理
        #url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=955742122799513&num=100&area=%E5%A4%A7%E9%99%86&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&sep=1'
        # 代理666
        #url = 'http://qsdrk.daili666api.com/ip/?tid=559017461234554&num=100&delay=3&category=2&sortby=time&foreign=none&filter=on'
        url = 'http://qsdrk.daili666api.com/ip/?tid=555451817416492&num=100&delay=3&category=2&sortby=time&foreign=none&filter=on'
        r = requests.get(url)
        lines = r.text.split()
        for line in lines:
            logger.debug(line)
            try:
                host, port = line.split(':')
                Proxy.objects.get_or_create(host=host, port=int(port))
            except Exception as e:
                print e
