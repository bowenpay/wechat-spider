# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
import requests
import json
from io import StringIO
from lxml import etree
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from wechatspider.util import get_redis
from wechat.constants import KIND_HISTORY
from .forms import WechatForm, HistoryForm, WechatConfigForm
from .models import Wechat, Topic


def index(request):
    context = {}
    params = request.GET.copy()
    _obj_list = Wechat.objects.filter().order_by('-id')

    paginator = Paginator(_obj_list, 20)  # Show 20 contacts per page

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
    if request.method == 'GET':
        return render_to_response('wechat/add.html', {
            "active_nav": "wechats.add",
        }, context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = WechatForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("配置保存成功, 爬虫正在后台努力工作中...")
        else:
            return HttpResponse('添加失败,请重试. 错误: %s' % form.errors)


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
        origin_history_start, origin_history_end = wechat.history_start, wechat.history_end
        form = WechatConfigForm(request.POST, instance=wechat)
        if form.is_valid():
            if (form.cleaned_data['history_start'] != origin_history_start
                or form.cleaned_data['history_end'] != origin_history_end):
                print '###############changed'
                data = {
                    'kind': KIND_HISTORY,
                    'wechat_id': wechat.id,
                    'wechatid': wechat.wechatid,
                    'history_start': '%s' % wechat.history_start,
                    'history_end': '%s' % wechat.history_end
                }
                r = get_redis()
                r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(data))
            else:
                print '#################not changed'
            form.save()
            messages.success(request, '保存成功.')
            return redirect(reverse('wechat.edit', kwargs={"id_": id_}))

        else:
            messages.error(request, '保存失败,请重试. 错误: %s' % form.errors)
            return redirect(reverse('users.user', kwargs={"id_": id_}))



def wechat_topics(request, id_):
    wechat = get_object_or_404(Wechat, pk=id_)
    context = {}
    # 文章信息
    params = request.GET.copy()
    _obj_list = Topic.objects.filter(wechat=wechat).order_by('-publish_time')

    paginator = Paginator(_obj_list, 3 )  # Show 10 contacts per page

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


def history(request):
    print request.POST
    wechatid = request.POST['wechatid']
    wechat = get_object_or_404(Wechat, wechatid=wechatid)

    form = HistoryForm(request.POST)
    if form.is_valid():
        wechat.history_start = form.cleaned_data['history_start']
        wechat.history_end = form.cleaned_data['history_end']
        wechat.save()
        data = {
            'kind': KIND_HISTORY,
            'wechat_id': wechat.id,
            'wechatid': wechat.wechatid,
            'history_start': '%s' % wechat.history_start,
            'history_end': '%s' % wechat.history_end
        }
        r = get_redis()
        r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(data))
        return HttpResponse("提交成功, 爬虫正在后台努力工作中...")
    else:
        return HttpResponse('设置失败,请重试. 错误: %s' % form.errors)


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
        wechatid = node.find(".//h4/span/label").text
        intro_node = node.find(".//p/span[2]")
        intro = ''.join([x for x in intro_node.itertext() if x not in ["red_beg", "red_end"]])
        url = 'http://weixin.sogou.com' + node.attrib['href']

        wechats.append({
            "name": name,
            "wechatid": wechatid,
            "avatar": avatar,
            "intro": intro,
            "url": url
        })

    return wechats