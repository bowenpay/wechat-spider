# 微信爬虫
一个爬取微信公众号文章的爬虫

# 安装

1）python环境, 检查python的版本，是否为2.7.x，如果不是，安装2.7.6。

centos 6.x 升级python2.6到python2.7,参考教程 http://ruiaylin.github.io/2014/12/12/python%20update/

2）安装依赖包, clone代码
安装Mysql-python依赖
```
yum install python-devel mysql-devel gcc
```

安装lxml依赖
```
yum install libxslt-devel libxml2-devel
```

安装浏览器环境 selenium依赖
```
yum install xorg-x11-server-Xvfb
yum install firefox
```

clone代码,安装依赖python库
```
$ git clone https://git.coding.net/xtwxx/No1022_Wechat-article-crawler.git
$ cd No1022_Wechat-article-crawler
$ pip install -r requirements.txt
```

在 wechatspider 目录下,添加 `local_settings.py` 文件,配置如下:
```
# -*- coding: utf-8 -*-
CRAWLER_DEBUG = True

# aliyun oss2
OSS2_CONFIG = {
    "ACCESS_KEY_ID": "NNV6RHQGNCH3M3yK",
    "ACCESS_KEY_SECRET": "1e214PQr7xZs9tcbNONF0WKENTfEna",
    "ENDPOINT": "",
    "BUCKET_DOMAIN": "oss-cn-hangzhou.aliyuncs.com",
    "BUCKET_NAME": "tingping",
    "IMAGES_PATH": "images/",
    "VIDEOS_PATH": "videos/",
    "CDN_DOMAIN": "tingping.oss-cn-hangzhou.aliyuncs.com"
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'wechatspider',
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS':{
            'charset': 'utf8mb4',
        },
    }
}
```

3) 初始化mysql

a) 安装mysql-server后，记得设置字符为utf8mb4。在my.cnf中设置：

```
[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

b) 重启数据库

c) 创建数据库wechatspider

```
mysql> CREATE DATABASE `wechatspider` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

d) 初始化表
```
$ python manage.py migrate
```

5）运行

```
python manage.py runserver 0.0.0.0:8001
```
访问 http://localhost:8001/。 测试没问题后，参考后面的supervisor脚本启动。

6) 创建超级管理员账号,访问后台
```
python manage.py createsuperuser
```

# 部署nginx
前期先用nginx将域名www.mydomain.com转发到8001端口。

# 部署supervisor脚本
参考文件 `supervisord.conf`

# 部署crontab脚本
参考文件 `crontab`
