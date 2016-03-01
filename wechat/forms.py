# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django import forms
from .models import Wechat


class WechatForm(forms.ModelForm):
    class Meta:
        model = Wechat
        fields = ['avatar', 'name', 'wechatid', 'url', 'intro', 'frequency']


class HistoryForm(forms.ModelForm):
    class Meta:
        model = Wechat
        fields = ['history_start', 'history_end']


class WechatConfigForm(forms.ModelForm):
    class Meta:
        model = Wechat
        fields = ['frequency', 'history_start', 'history_end']