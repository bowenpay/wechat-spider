# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import urllib
import socket
import time

def get_ip():
    exip = ''
    ipList = socket.gethostbyname_ex(socket.gethostname())

    for itemList in ipList:
        if isinstance(itemList, list):
                for ip in itemList:
                    print '####:',ip
                    if ip not in ['192.168.11.58']:
                        exip = ip
    return exip


def save_ip(exip):
    if exip:
        params = urllib.urlencode({'host': exip, 'port': 808})
        f = urllib.urlopen("http://wechatspider.0fenbei.com/wechat/proxy/1/edit/", params)
        print f.read()

if __name__ == '__main__':
    while True:
        try:
            exip = get_ip()
            print 'new ip:', exip
            save_ip(exip)
        except Exception as e:
            print e
        finally:
            print 'sleep 1 second'
            time.sleep(1)

