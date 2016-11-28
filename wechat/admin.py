from django.contrib import admin
from .models import Wechat, Topic, Proxy, Word


class WechatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wechatid')
    search_fields = ['name']

admin.site.register(Wechat, WechatAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'wechat')
    search_fields = ['title']

admin.site.register(Topic, TopicAdmin)


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('kind', 'host', 'port', 'speed', 'status', 'retry')
    list_filter = ('kind', 'status')


class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'kind', 'text', 'intro', 'frequency', 'next_crawl_time')
    list_filter = ['kind']
    search_fields = ['text']


admin.site.register(Word, WordAdmin)
admin.site.register(Proxy, ProxyAdmin)
