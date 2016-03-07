# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
import platform
import requests
from datetime import datetime, timedelta
from dateutil.parser import parse
from random import sample, randint
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from wechatspider.util import get_uniqueid
from wechat.models import Topic

import logging
logger = logging.getLogger()


class RequestsDownloaderBackend(object):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        self.proxy = proxy

    def format_proxies(self):
        p = self.proxy
        if self.proxy:
            if p.user:
                data = 'http://%s:%s@%s:%s' % (p.user, p.password, p.host, p.port)
            else:
                data = 'http://%s:%s' % (p.host, p.port)
            return {
                "http": data
            }
        else:
            return None

    def download(self, url):
        header = sample(self.headers, 1)[0]
        proxies = self.format_proxies()
        if isinstance(url, basestring):
            rsp = requests.get(url, headers=header, proxies=proxies)
            rsp.close()
            rsp.encoding = rsp.apparent_encoding
            return rsp.text
        elif isinstance(url, dict):
            link, method, data, data_type = url.get('url'), url.get('method'), url.get('data'), url.get('dataType')
            req = {'GET': requests.get, 'POST': requests.post}.get(method)
            rsp = req(link, data=data, headers=header, proxies=proxies)
            rsp.close()
            rsp.encoding = rsp.apparent_encoding
            if data_type == 'json':
                return rsp.json()
            else:
                return rsp.text


class BrowserDownloaderBackend(object):
    def download(self):
        pass


BROWSER = None


def get_browser():
    global BROWSER
    if not BROWSER:
        if platform.system() != 'Darwin':
            # 不是mac系统, 启动窗口
            display = Display(visible=0, size=(1024, 768))
            display.start()
        # 启动浏览器
        BROWSER = webdriver.Firefox()
    return BROWSER


class SeleniumDownloaderBackend(object):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        # 设置代理
        self.proxy = proxy
        self.browser = get_browser()

    def __del__(self):
        pass
        # 关闭浏览器,关闭窗口
        #self.browser.close()
        #self.display.stop()

    def download(self, url):
        pass

    def visit_wechat_index(self, wechatid):
        browser = self.browser
        # 访问首页, 输入wchatid, 点击查询
        browser.get("http://weixin.sogou.com/")
        print browser.title
        element_querybox = browser.find_element_by_name('query')
        element_querybox.send_keys(wechatid, Keys.ARROW_DOWN)
        element_search_btn = browser.find_element_by_xpath("//input[@value='搜公众号']")
        element_search_btn.click()
        time.sleep(2)
        print browser.title

    def visit_wechat_topic_list(self):
        browser = self.browser
        # 找到搜索列表第一个微信号, 点击打开新窗口
        element_wechat = browser.find_element_by_xpath("//div[@class='txt-box']/h3")
        element_wechat.click()
        time.sleep(2)
        # 切到当前的文章列表页窗口
        new_handler = browser.window_handles[-1]
        browser.switch_to.window(new_handler)
        time.sleep(2)

    def get_publish_time(self, txt):
        if '小时前' in txt:
            res = datetime.now()
        elif '天前' in txt:
            days = int(txt.split('天前')[0])
            res = datetime.now() - timedelta(days=days)
        else:
            try:
                res = parse(txt)
            except Exception as e:
                logger.exception(e)
                res = datetime.now()
        return res

    def visit_wechat_history_topic_list(self, history_start):
        browser = self.browser
        start_time = parse(history_start)
        # 找到搜索列表第一个微信号, 点击打开新窗口
        element_publish_times = browser.find_elements_by_xpath("//div[@class='s-p']")
        if len(element_publish_times) > 1:
            element_publish_time = element_publish_times[-1]
        else:
            return

        txt_publish_time = element_publish_time.text.strip()
        publish_time = self.get_publish_time(txt_publish_time)
        if publish_time > start_time:
            element_wxmore = browser.find_element_by_id("wxmore")
            if element_wxmore.is_displayed():
                element_wxmore.click()
                time.sleep(2)
                self.visit_wechat_history_topic_list(history_start)
            else:
                return

    def download_wechat_topics(self, wechat_id, process_topic):
        browser = self.browser
        elems = browser.find_elements_by_xpath("//div[@class='txt-box']/h4/a")
        elems_avatars = browser.find_elements_by_xpath("//div[@class='img_box2']//img")
        avatars = [item.get_attribute('src').split('url=')[1] for item in elems_avatars]
        print '###############', elems
        links = []
        for idx, item in enumerate(elems):
            title = item.text.strip()
            print title
            uniqueid = get_uniqueid('%s:%s' % (wechat_id, title))
            try:
                Topic.objects.get(uniqueid=uniqueid)
            except Topic.DoesNotExist:
                links.append((title, item.get_attribute('href'), avatars[idx]))
                logger.debug('文章不存在, title=%s, uniqueid=%s' % (title, uniqueid))
        for title, link, avatar in links:
            # 可以访问了
            browser.get(link)
            time.sleep(2)

            if 'antispider' in browser.current_url:
                """被检测出爬虫了"""
                time.sleep(randint(60, 120))
            else:
                js = """
                    var imgs = document.getElementsByTagName('img');

                    for(var i = 0; i < imgs.length; i++) {
                      var dataSrc = imgs[i].getAttribute('data-src');
                      if (dataSrc){
                        imgs[i].setAttribute('src', dataSrc);
                      }
                    }
                    return document.documentElement.innerHTML;
                """
                body = browser.execute_script(js)
                process_topic({
                    'url': browser.current_url,
                    'body': body,
                    'avatar': avatar,
                    'title': title
                })
                time.sleep(randint(10, 20))

    def clean_wechat_browser(self):
        browser = self.browser
        # 关闭其它窗口,只留一个
        current_hander = browser.current_window_handle
        all_handlers = browser.window_handles[:]

        def close_window(handler):
            browser.switch_to.window(handler)
            browser.close()
        if len(all_handlers) > 1:
            map(close_window, filter(lambda item: item != current_hander, all_handlers))
            browser.switch_to.window(current_hander)
        # 清空cookie,恢复初始状态
        browser.delete_all_cookies()


    def download_wechat(self, data, process_topic):
        wechat_id, wechatid = data['wechat_id'], data['wechatid']
        topics = []
        try:
            self.visit_wechat_index(wechatid)
            self.visit_wechat_topic_list()
            self.download_wechat_topics(wechat_id, process_topic)
        except Exception as e:
            logger.exception(e)
        finally:
            self.clean_wechat_browser()

        return topics

    def download_wechat_history(self, data, process_topic):
        wechat_id, wechatid, history_start, history_end = data['wechat_id'], data['wechatid'], data['history_start'], data['history_end']
        topics = []
        try:
            self.visit_wechat_index(wechatid)
            self.visit_wechat_topic_list()
            self.visit_wechat_history_topic_list(history_start)
            self.download_wechat_topics(wechat_id, process_topic)
        except Exception as e:
            logger.exception(e)
        finally:
            self.clean_wechat_browser()