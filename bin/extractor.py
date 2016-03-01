# -*- coding: utf-8 -*-
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

import json
from django.conf import settings
from wechatspider.util import get_redis, get_uniqueid
from wechat.extractors import XPathExtractor, PythonExtractor, ImageExtractor, VideoExtractor
import logging
logger = logging.getLogger()

DETAIL_RULES = [
  {
    "key":"avatar",
    "rules":[
      {
        "kind":"python",
        "data":"out_val=data['avatar'];"
      }
    ]
  },
  {
    "key":"title",
    "rules":[
      {
        "kind":"xpath",
        "data":"//h2[@id='activity-name']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=' '.join([item.strip() for item in in_val])"
      }
    ]
  },
  {
    "key":"content",
    "rules":[
      {
        "kind":"xpath",
        "data":"//div[@id='js_content']"
      },
      {
        "kind":"python",
        "data":"from lxml import html;out_val=''.join([html.tostring(child, encoding='unicode') for child in in_val])"
      },
      {
        "kind":"python",
        "data":"import re;out_val=re.subn(r'<(script).*?</\\1>(?s)', '', in_val)[0];"
      }
    ]
  },
  {
    "key":"publish_time",
    "rules":[
      {
        "kind":"xpath",
        "data":"//em[@id='post-date']/text()"
      },
      {
        "kind":"python",
        "data":"from datetime import datetime;date_str=in_val[0].strip().split()[0];out_val=datetime.strptime(date_str, '%Y-%m-%d')"
      },
      {
        "kind":"python",
        "data":"from datetime import datetime;now=datetime.now();out_val = str(in_val.replace(microsecond=now.microsecond) if isinstance(in_val, datetime) else datetime.now())"
      }
    ]
  }
];

class Extractor(object):
    def __init__(self):
        self.redis = get_redis()

    def extract(self, content, rules, context):
        res = content
        for rule in rules:
            extractor = None
            if rule["kind"] == "xpath":
                extractor = XPathExtractor(res, rule["data"])
            elif rule["kind"] == "python":
                extractor = PythonExtractor(rule["data"], res, context=context)
            elif rule["kind"] == "image":
                extractor = ImageExtractor(res)
            elif rule["kind"] == "video":
                extractor = VideoExtractor(res)

            res = extractor.extract()

        return res

    def get_detail(self, content, data):
        result = {
            "wechat_id": data["wechat_id"],
            "url": data["url"],
            "source": data["body"],
            "avatar": data["avatar"]
        }
        rules = DETAIL_RULES
        for item in rules:
            col = item["key"]
            print col
            col_rules = item["rules"]
            col_value = self.extract(content, col_rules, {'data': result})
            result[col] = col_value

        # 解析结束, 保存
        self.redis.lpush(settings.CRAWLER_CONFIG["processor"], json.dumps(result))
        result["source"] = ""
        result["content"] = ""
        logger.debug('extracted:%s' % result)

    def run(self):
        r = self.redis
        if settings.CRAWLER_DEBUG:
            r.delete(settings.CRAWLER_CONFIG["extractor"])
        while True:
            try:
                data = r.brpop(settings.CRAWLER_CONFIG["extractor"])
            except Exception as e:
                print e
                continue
            #print data
            data = json.loads(data[1])
            body = data['body']
            # 如果没有多项详情,则只是单项
            self.get_detail(body, data)


if __name__ == '__main__':
    my_extractor = Extractor()
    my_extractor.run()
