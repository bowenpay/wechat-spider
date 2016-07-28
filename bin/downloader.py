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
from wechat.constants import KIND_HISTORY, KIND_DETAIL, KIND_KEYWORD
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
                        if topic.get('kind', None) == KIND_DETAIL:
                            item_data = topic
                        elif topic.get('kind', None) == KIND_KEYWORD:
                            item_data = topic
                        else:
                            item_data = topic
                            item_data["wechat_id"] = data["wechat_id"]
                        r.lpush(CRAWLER_CONFIG["extractor"], json.dumps(item_data))
                        logger.debug(item_data)

                    with SeleniumDownloaderBackend(proxy=proxy) as browser:
                        if data.get('kind') == KIND_DETAIL:
                            res = browser.download_wechat_topic_detail(data, process_topic)
                        elif data.get('kind') == KIND_HISTORY:
                            #res = browser.download_wechat_history(data, process_topic)
                            pass
                        elif data.get('kind') == KIND_KEYWORD:
                            res = browser.download_wechat_keyword(data, process_topic)
                        else:
                            res = browser.download_wechat(data, process_topic)

                    time.sleep(randint(1, 5))
            except Exception as e:
                print e
                raise


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
