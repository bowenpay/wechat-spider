# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
import requests
from io import StringIO
from lxml import etree
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import WechatForm, HistoryForm, WechatConfigForm
from .models import Wechat


def index(request):
    context = {}
    params = request.GET.copy()
    _obj_list = Wechat.objects.filter().order_by('-id')

    paginator = Paginator(_obj_list, 2)  # Show 25 contacts per page

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
        form = WechatConfigForm(instance=wechat)
        return render_to_response('wechat/edit.html', {}, context_instance=RequestContext(request, {
            "active_nav": "wechats",
            "wechat": wechat,
            "form": form
        }))
    elif request.method == 'POST':
        form = WechatConfigForm(request.POST, instance=wechat)
        if form.is_valid():
            form.save()
            messages.success(request, '保存成功.')
            return redirect(reverse('wechat.edit', kwargs={"id_": id_}))

        else:
            messages.error(request, '保存失败,请重试. 错误: %s' % form.errors)
            return redirect(reverse('users.user', kwargs={"id_": id_}))


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