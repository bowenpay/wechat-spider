# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
from django.core.management.base import BaseCommand
from wechat.models import Proxy
from wechat.util import check_proxy
import requests

class Command(BaseCommand):
    help = 'get proxies'

    def handle(self, *args, **options):
        while True:
            self.get_proxies()
            time.sleep(10)

    def get_proxies(self):
        url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=955742122799513&num=100&area=%E5%A4%A7%E9%99%86&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&sep=1'
        r = requests.get(url)
        lines = r.text.split()
        for line in lines:
            print line
            try:
                host, port = line.split(':')
                Proxy.objects.get_or_create(host=host, port=int(port))
            except Exception as e:
                print e