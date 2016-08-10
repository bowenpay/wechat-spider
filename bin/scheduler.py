# -*- coding: utf-8 -*-
__author__ = 'yijingping'
# 加载django环境
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wechatspider.settings'
import django
django.setup()

import json
from wechat.models import Wechat, Word
from django.conf import settings
import logging
logger = logging.getLogger()
from datetime import datetime, timedelta
import time
from wechatspider.util import get_redis
from wechat.constants import KIND_NORMAL, KIND_KEYWORD


class Scheduler(object):
    def run(self):
        r = get_redis()
        if settings.CRAWLER_DEBUG:
            r.delete(settings.CRAWLER_CONFIG["downloader"])

        while True:
            now = datetime.now()
            # 获取要抓取的公众号
            wechats = Wechat.objects.filter(frequency__gt=0, next_crawl_time__lt=now, status=Wechat.STATUS_DEFAULT).order_by('-id')
            for item in wechats:
                data = {
                    'kind': KIND_NORMAL,
                    'wechat_id': item.id,
                    'wechatid': item.wechatid
                }

                r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(data))

                # 更新index_rule
                item.next_crawl_time = now + timedelta(minutes=item.frequency)
                #item.next_crawl_time = now + timedelta(seconds=item.frequency)
                item.save()

                logging.debug(data)

            # 获取要抓取的关键词
            keywords = Word.objects.filter(frequency__gt=0, next_crawl_time__lt=now).order_by('-id')
            for item in keywords:
                data = {
                    'kind': KIND_KEYWORD,
                    'word': item.text
                }

                r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(data))

                # 更新index_rule
                item.next_crawl_time = now + timedelta(minutes=item.frequency)
                #item.next_crawl_time = now + timedelta(seconds=item.frequency)
                item.save()

                logging.debug(data)

            time.sleep(1)

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
