# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
import urllib2
import requests
from lxml.etree import tostring
from itertools import chain

ip_check_url = 'http://api.ipify.org'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
socket_timeout = 3


# Get real public IP address
def get_real_pip():
    req = urllib2.Request(ip_check_url)
    req.add_header('User-agent', user_agent)
    conn = urllib2.urlopen(req)
    page = conn.read()
    conn.close()
    return page

# Set global variable containing "real" public IP address
real_pip = get_real_pip()


def check_proxy(host, port):
    try:
        # Build opener
        proxy_handler = urllib2.ProxyHandler({'http': '%s:%s' % (host, port)})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', user_agent)]
        urllib2.install_opener(opener)

        # Build, time, and execute request
        req = urllib2.Request(ip_check_url)
        time_start = time.time()
        conn = urllib2.urlopen(req, timeout=socket_timeout)
        time_end = time.time()
        detected_pip = conn.read()
        conn.close()

        # Calculate request time
        time_diff = time_end - time_start

        # Check if proxy is detected
        if detected_pip == real_pip:
            proxy_detected = False
        else:
            proxy_detected = True

    # Catch exceptions
    except urllib2.HTTPError, e:
        print "ERROR: Code ", e.code
        return (True, False, 999)
    except Exception, detail:
        print "ERROR: ", detail
        return (True, False, 999)

    # Return False if no exceptions, proxy_detected=True if proxy detected
    return (False, proxy_detected, time_diff)


def check_wechat(host, port):
    try:
        time_start = time.time()
        # Build opener
        proxies = {
            'http': 'http://%s:%s' % (host, port)
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
        rsp = requests.get("http://weixin.sogou.com/weixin",
                           params={"type": 1, "query": "金融"},
                           proxies=proxies, headers=headers,
                           timeout=1
        )
        rsp.close()
        time_end = time.time()

        # Calculate request time
        time_diff = time_end - time_start

        #print rsp.content
        # Check if proxy is detected
        if '金融的相关微信公众号' in rsp.content:
            proxy_detected = True
            print rsp.content
        else:
            proxy_detected = False

    # Catch exceptions
    except urllib2.HTTPError, e:
        print "ERROR: Code ", e.code
        return (True, False, 999)
    except Exception, detail:
        print "ERROR: ", detail
        return (True, False, 999)

    # Return False if no exceptions, proxy_detected=True if proxy detected
    return (False, proxy_detected, time_diff)


def stringify_children(node):
    return "".join([x for x in node.itertext()])
