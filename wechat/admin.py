from django.contrib import admin
from .models import Wechat, Topic, Proxy


class WechatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wechatid')

admin.site.register(Wechat, WechatAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'wechat')

admin.site.register(Topic, TopicAdmin)


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'speed', 'status', 'retry')
    list_filter = ('status',)

admin.site.register(Proxy, ProxyAdmin)