# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
import json
import requests
from io import StringIO
from lxml import etree
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from wechat.constants import KIND_DETAIL
from wechatspider.util import get_redis
from .forms import WechatForm, WechatConfigForm
from .models import Wechat, Topic, Proxy
from .extractors import download_to_oss


def index(request):
    context = {}
    params = request.GET.copy()
    _obj_list = Wechat.objects.filter().order_by('-id')

    paginator = Paginator(_obj_list, 50)  # Show 20 contacts per page

    page = request.GET.get('page')
    try:
        _objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _objs = paginator.page(paginator.num_pages)

    context.update({
        "active_nav": "wechats",
        "wechats": _objs,
        "params": params
    })

    return render_to_response('wechat/index.html', RequestContext(request, context))


def add(request):
    if request.method == 'POST':
        form = WechatForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.avatar = download_to_oss(obj.avatar, settings.OSS2_CONFIG["IMAGES_PATH"])
            obj.qrcode = download_to_oss(obj.qrcode, settings.OSS2_CONFIG["IMAGES_PATH"])
            obj.save()
            messages.success(request, '保存成功.')
            return redirect(reverse('wechat.index'))
        else:
            messages.error(request, '添加失败,请重试. 错误: %s' % form.errors)
            return redirect(reverse('wechat.index'))


def edit(request, id_):
    wechat = get_object_or_404(Wechat, pk=id_)
    if request.method == 'GET':
        context = {}
        # 编辑信息
        form = WechatConfigForm(instance=wechat)
        context.update({
            "active_nav": "wechats",
            "wechat": wechat,
            "form": form
        })
        return render_to_response('wechat/edit.html', {}, context_instance=RequestContext(request, context))
    elif request.method == 'POST':
        form = WechatConfigForm(request.POST, instance=wechat)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.next_crawl_time = datetime.now()
            messages.success(request, '保存成功.')
            return redirect(reverse('wechat.edit', kwargs={"id_": id_}))

        else:
            messages.error(request, '保存失败,请重试. 错误: %s' % form.errors)
            return redirect(reverse('wechat.edit', kwargs={"id_": id_}))


def topic_list(request):
    context = {}
    # 文章信息
    params = request.GET.copy()
    _obj_list = Topic.objects.order_by('-publish_time')

    paginator = Paginator(_obj_list, 50 )  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        _objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _objs = paginator.page(paginator.num_pages)

    context.update({
        "active_nav": "topics",
        "topics": _objs,
        "params": params
    })
    return render_to_response('wechat/topic_list.html', {}, context_instance=RequestContext(request, context))


def wechat_topics(request, id_):
    wechat = get_object_or_404(Wechat, pk=id_)
    context = {}
    # 文章信息
    params = request.GET.copy()
    _obj_list = Topic.objects.filter(wechat=wechat).order_by('-publish_time')

    paginator = Paginator(_obj_list, 50 )  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        _objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _objs = paginator.page(paginator.num_pages)

    context.update({
        "active_nav": "wechats",
        "wechat": wechat,
        "topics": _objs,
        "params": params
    })
    return render_to_response('wechat/wechat_topics.html', {}, context_instance=RequestContext(request, context))


def topic_detail(request, id_):
    topic = get_object_or_404(Topic, pk=id_)
    return render_to_response('wechat/topic_detail.html', {}, context_instance=RequestContext(request, {
        "topic": topic
    }))


def topic_add(request):
    url = request.POST.get('url', '')
    if url.startswith('http://mp.weixin.qq.com/'):
        data = {
            'kind': KIND_DETAIL,
            'url': url
        }

        r = get_redis()
        r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(data))
        messages.success(request, '链接已经提交给爬虫,稍后查看爬取结果.')
    else:
        messages.error(request, 'url 错误, 添加失败')
    return redirect(reverse('wechat.topic_list'))



def search(request):
    query = request.GET.get('query')
    wechats = searcy_wechat(query)
    return render_to_response('wechat/search_content.html', RequestContext(request, {"wechats": wechats}))


def searcy_wechat(query):
    p = Proxy.objects.filter(status=Proxy.STATUS_SUCCESS).order_by('?').first()
    if p:
        proxies = {
            'http': 'http://%s:%s' % (p.host, p.port)
        }
    else:
        proxies = {}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
    }
    rsp = requests.get("http://weixin.sogou.com/weixin",
                       params={"type": 1, "query": query},
                       proxies=proxies, headers=headers
    )
    rsp.close()
    rsp.encoding = rsp.apparent_encoding
    #print rsp.content
    htmlparser = etree.HTMLParser()
    tree = etree.parse(StringIO(rsp.text), htmlparser)
    nodes = tree.xpath('//div[contains(@class,"wx-rb")]')
    wechats = []
    for node in nodes:
        name =  ''.join([x for x in node.find(".//h3").itertext() if x not in ["red_beg", "red_end"]])
        avatar = node.find('.//img').attrib['src']
        qrcode = node.find(".//div[@class='pos-box']/img").attrib['src']
        wechatid = node.find(".//h4/span/label").text
        intro_node = node.find(".//p/span[2]")
        intro = ''.join([x for x in intro_node.itertext() if x not in ["red_beg", "red_end"]])

        wechats.append({
            "name": name,
            "wechatid": wechatid,
            "avatar": avatar,
            "qrcode": qrcode,
            "intro": intro
        })

    return wechats