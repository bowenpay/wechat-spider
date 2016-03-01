# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
import requests
from random import sample
from selenium import webdriver

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


class SeleniumDownloaderBackend(object):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        self.proxy = proxy

    def download(self, url):
        pass

    def download_wechats(self, url):
        res = []
        browser = webdriver.Firefox()
        browser.get(url)
        time.sleep(20)
        elems = browser.find_elements_by_xpath("//div[@class='txt-box']/h4/a")
        links = [item.get_attribute('href') for item in elems]
        for link in links:
            # 检查访问间隔限制,等待直至可以访问
            # TODO
            # 可以访问了
            browser.get(link)
            res.append({
                'url': browser.current_url,
                'body': browser.page_source,
                'avatar': ''
            })
            time.sleep(10)
        browser.close()
        return res
