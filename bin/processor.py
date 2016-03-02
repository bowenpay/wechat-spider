# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
# 加载django环境
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8') 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wechatspider.settings'
import django
django.setup()

import _mysql
from datetime import datetime
import json
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
from wechat.models import Topic
from wechat.processors import DjangoModelBackend
from wechatspider.util import get_redis, get_uniqueid
import logging
logger = logging.getLogger()


class Processor():
    def __init__(self):
        self.pools = {}

    def get_backends(self):
        backend = DjangoModelBackend(Topic)
        return [backend]

    def process(self, data):
        backends = self.get_backends()
        for backend in backends:
            backend.process(data)

    def run(self):
        r = get_redis()
        if settings.CRAWLER_DEBUG:
            r.delete(settings.CRAWLER_CONFIG["processor"])
        while True:
            try:
                rsp = r.brpop(settings.CRAWLER_CONFIG["processor"])
            except Exception as e:
                print e
                continue

            data = json.loads(rsp[1])
            logger.info(json.dumps(data, encoding="UTF-8", ensure_ascii=False))
            self.process(data)


if __name__ == '__main__':
    processor = Processor()
    processor.run()
