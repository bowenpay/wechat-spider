# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
import requests
from io import StringIO
from lxml import etree
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .forms import WechatForm, WechatConfigForm
from .models import Wechat, Topic
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
            form.save()
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



def search(request):
    query = request.GET.get('query')
    wechats = searcy_wechat(query)
    return render_to_response('wechat/search_content.html', RequestContext(request, {"wechats": wechats}))


def searcy_wechat(query):
    rsp = requests.get("http://weixin.sogou.com/weixin", params={"type": 1, "query": query})
    rsp.close()
    rsp.encoding = rsp.apparent_encoding

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