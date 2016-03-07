# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django import forms
from .models import Wechat


class WechatForm(forms.ModelForm):
    class Meta:
        model = Wechat
        fields = ['avatar', 'qrcode', 'name', 'wechatid', 'intro', 'frequency']


class WechatConfigForm(forms.ModelForm):
    class Meta:
        model = Wechat
        fields = ['frequency']