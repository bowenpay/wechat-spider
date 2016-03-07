# -*- coding: utf-8 -*-
# 加载django环境
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wechatspider.settings'
import django
django.setup()

import time
import json
from random import randint
from django.conf import settings
from wechatspider.util import get_redis
from wechat.proxies import MysqlProxyBackend
from wechat.downloaders import SeleniumDownloaderBackend
from wechat.constants import KIND_HISTORY
import logging
logger = logging.getLogger()

CRAWLER_CONFIG = settings.CRAWLER_CONFIG
CRAWLER_GLOBAL_LIMIT_SPEED = settings.CRAWLER_GLOBAL_LIMIT_SPEED


class Downloader(object):
    def __init__(self):
        self.redis = get_redis()

    def get_proxy(self):
        return MysqlProxyBackend()

    def check_limit_speed(self):
            proxy = self.get_proxy()
            key = '%s:%s' % (CRAWLER_CONFIG['global_limit_speed'], proxy)
            if self.redis.exists(key):
                return True, proxy
            else:
                self.redis.psetex(key, CRAWLER_GLOBAL_LIMIT_SPEED, CRAWLER_GLOBAL_LIMIT_SPEED)
                return False, proxy

    def run(self):
        r = self.redis
        if settings.CRAWLER_DEBUG:
            r.delete(CRAWLER_CONFIG["downloader"])
        while True:
            try:
                resp_data = r.brpop(settings.CRAWLER_CONFIG["downloader"])
            except Exception as e:
                print e
                continue

            try:
                data = json.loads(resp_data[1])

                logger.debug(data)
                is_limited, proxy = self.check_limit_speed()
                if is_limited:
                    print '# 被限制, 放回去, 下次下载'
                    time.sleep(1)  # 休息一秒, 延迟放回去的时间
                    r.lpush(CRAWLER_CONFIG["downloader"], resp_data[1])
                else:
                    print '# 未被限制,可以下载'
                    # 处理文章的函数,用于回调. 每下载一篇, 处理一篇
                    def process_topic(topic):
                        item_data = {
                            "wechat_id": data["wechat_id"],
                            "title": topic["title"],
                            "url": topic["url"],
                            "body": topic["body"],
                            "avatar": topic["avatar"],
                        }
                        r.lpush(CRAWLER_CONFIG["extractor"], json.dumps(item_data))
                        logger.debug(item_data)

                    browser = SeleniumDownloaderBackend(proxy=proxy)
                    if data.get('kind') == KIND_HISTORY:
                        res = browser.download_wechat_history(data, process_topic)
                    else:
                        res = browser.download_wechat(data, process_topic)

                    time.sleep(randint(20, 30))
            except Exception as e:
                print e
                raise


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
