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
from wechat.extractors import XPathExtractor, PythonExtractor, ImageExtractor, VideoExtractor, WechatContentExtractor
from wechat.constants import KIND_HISTORY, KIND_DETAIL, KIND_KEYWORD
import logging
logger = logging.getLogger()

NORMAL_RULES = [
  {
    "key":"avatar",
    "rules":[
      {
        "kind":"python",
        "data":"out_val=data['avatar'];"
      },
      {
        "kind":"image",
        "data":""
      }
    ]
  },
  {
    "key":"origin_title",
    "rules":[
      {
        "kind":"xpath",
        "data":"//title/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[0] if in_val else '';"
      }
    ]
  },
  {
    "key":"source",
    "rules":[
      {
          "kind":"image",
          "data":""
      },
      {
        "kind":"WechatContent",
        "data":""
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
          "kind":"image",
          "data":""
      },
      {
        "kind":"WechatContent",
        "data":""
      }
    ]
  },
  {
    "key":"words",
    "rules":[
      {
        "kind":"xpath",
        "data":"//div[@id='js_content']//text()"
      },
      {
        "kind":"python",
        "data":"out_val=sum([len(item.strip()) for item in in_val])"
      }
    ]
  },
  {
    "key":"publish_time",
    "rules":[
      {
        "kind":"python",
        "data":"from datetime import datetime;out_val = str(datetime.now());"
      }
    ]
  },
  {
    "key": "read_num",
    "rules": [
      {
        "kind": "xpath",
        "data": "//span[@id='sg_readNum3']/text()"
      },
      {
        "kind": "python",
        "data": "out_val=sum([int(item.strip().strip('+')) for item in in_val])"
      }
    ]
  },
  {
    "key": "like_num",
    "rules": [
      {
        "kind":"xpath",
        "data":"//span[@id='sg_likeNum3']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=sum([int(item.strip().strip('+')) for item in in_val])"
      }
    ]
  }
]

DETAIL_RULES = [
  {
    "key":"title",
    "rules":[
      {
        "kind":"xpath",
        "data":"//title/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[0] if in_val else '';"
      }
    ]
  },
  {
    "key":"origin_title",
    "rules":[
      {
        "kind":"xpath",
        "data":"//title/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[0] if in_val else '';"
      }
    ]
  },
  {
    "key":"source",
    "rules":[
      {
          "kind":"image",
          "data":""
      },
      {
        "kind":"WechatContent",
        "data":""
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
          "kind":"image",
          "data":""
      },
      {
        "kind":"WechatContent",
        "data":""
      }
    ]
  },
  {
    "key":"words",
    "rules":[
      {
        "kind":"xpath",
        "data":"//div[@id='js_content']//text()"
      },
      {
        "kind":"python",
        "data":"out_val=sum([len(item.strip()) for item in in_val])"
      }
    ]
  },
  {
    "key":"abstract",
    "rules":[
      {
        "kind":"xpath",
        "data":"//div[@id='js_content']//text()"
      },
      {
        "kind":"python",
        "data":"tmp=''.join([item.strip() for item in in_val]);out_val = '%s...' % tmp[:220] if len(tmp) > 220 else tmp;"
      }
    ]
  },
  {
    "key":"avatar",
    "rules":[
      {
        "kind":"python",
        "data":"out_val=data['content'];"
      },
      {
        "kind":"xpath",
        "data":"//img/@src"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[1] if len(in_val) > 1 else '';"
      }
    ]
  },
  {
    "key":"publish_time",
    "rules":[
      {
        "kind":"python",
        "data":"from datetime import datetime;out_val = str(datetime.now());"
      }
    ]
  },
  {
    "key":"wechatid",
    "rules":[
      {
        "kind":"xpath",
        "data":"//span[@class='profile_meta_value']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[0] if len(in_val) == 2 else '';"
      }
    ]
  },
  {
    "key":"name",
    "rules":[
      {
        "kind":"xpath",
        "data":"//strong[@class='profile_nickname']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[0] if in_val else '';"
      }
    ]
  },
  {
    "key":"intro",
    "rules":[
      {
        "kind":"xpath",
        "data":"//span[@class='profile_meta_value']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=in_val[1] if len(in_val) == 2 else '';"
      }
    ]
  },

  {
    "key":"qrcode",
    "rules":[
      {
        "kind":"xpath",
        "data":"//img[@id='js_pc_qr_code_img']/@src"
      },
      {
        "kind":"python",
        "data":"out_val='http://mp.weixin.qq.com' + in_val[0] if in_val else '';"
      }
    ]
  },
  {
    "key": "read_num",
    "rules": [
      {
        "kind": "xpath",
        "data": "//span[@id='sg_readNum3']/text()"
      },
      {
        "kind": "python",
        "data": "out_val=sum([int(item.strip().strip('+')) for item in in_val])"
      }
    ]
  },
  {
    "key": "like_num",
    "rules": [
      {
        "kind":"xpath",
        "data":"//span[@id='sg_likeNum3']/text()"
      },
      {
        "kind":"python",
        "data":"out_val=sum([int(item.strip().strip('+')) for item in in_val])"
      }
    ]
  }

]
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
            elif rule["kind"] == "WechatContent":
                extractor = WechatContentExtractor(res)

            res = extractor.extract()

        return res

    def get_detail(self, content, data):
        if data.get('kind') == KIND_DETAIL:
            result = {
                "kind": data["kind"],
                "url": data["url"],
                "source": data["body"],
                "avatar": ''
            }
            rules = DETAIL_RULES
        elif data.get('kind') == KIND_KEYWORD:
            result = {
                "kind": data["kind"],
                "url": data["url"],
                "source": data["body"],
                "avatar": ''
            }
            rules = DETAIL_RULES
        else:
            result = {
                "wechat_id": data["wechat_id"],
                "url": data["url"],
                "title": data["title"],
                "source": data["body"],
                "avatar": data["avatar"],
                "abstract": data["abstract"]
            }
            rules = NORMAL_RULES

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
