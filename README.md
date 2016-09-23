# 微信爬虫
一个爬取微信公众号文章的爬虫。 

# 微信爬虫的由来
零分贝是一家帮助中国5000万贫困人口与社会公益组织对接的公司。

我们通过国家和地方政府的“建档立卡”系统，获取到了一手的贫困户数据，目前有100万左右，总数为5000万，目前每个月都在增长。

为了帮助这部分贫困户对接公益机构，我写了这个微信爬虫，从微信公众号发布的文章中上找出最新的公益项目。

这种找项目的方式的可行性，我们还在试验中。 

起初，为了快速上线，本爬虫的代码是基于我的另一个 [通用爬虫项目](https://github.com/yijingping/unicrawler) 开发的，我也希望任何对本项目感兴趣的人联系我，与我一同改进这个项目。

联系方式：在本项目中新建一个issue留言。

# 界面预览

1） 要爬取的微信公众号列表

![](docs/images/1.jpg?raw=true)

2） 要爬取的文章关键字列表

![](docs/images/2.png?raw=true)

3） 已经爬取的微信文章

![](docs/images/3.png?raw=true)

4） 查看文章，并标记是否可用

![](docs/images/4.jpg?raw=true)

5） 控制爬取进程数

![](docs/images/5.png?raw=true)


# 安装

1）python环境, 检查python的版本，是否为2.7.x，如果不是，安装2.7.6。

centos 6.x 升级python2.6到python2.7,参考教程 http://ruiaylin.github.io/2014/12/12/python%20update/

如果是centos 7.x, 默认就是python2.7,不用升级

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
$ git clone https://github.com/bowenpay/wechat-spider.git
$ cd wechat-spider
$ pip install -r requirements.txt
```

在 wechatspider 目录下,添加 `local_settings.py` 文件,配置如下:
```
# -*- coding: utf-8 -*-
CRAWLER_DEBUG = True

# aliyun oss2, 可以将图片和视频存储到阿里云，也可以选择不存储，爬取速度会更快。
OSS2_CONFIG = {
    "ACCESS_KEY_ID": "XXXXXXXXXXXXXX",
    "ACCESS_KEY_SECRET": "YYYYYYYYYYYYYYYYYYYYYY",
    "ENDPOINT": "",
    "BUCKET_DOMAIN": "oss-cn-hangzhou.aliyuncs.com",
    "BUCKET_NAME": "XXXXX",
    "IMAGES_PATH": "images/",
    "VIDEOS_PATH": "videos/",
    "CDN_DOMAIN": "XXXXXX.oss-cn-hangzhou.aliyuncs.com"
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

SECRET_KEY="xxxxxx"
```

3) 初始化mysql

a) 安装mysql-server后([How to install in Centos](https://www.linode.com/docs/databases/mysql/how-to-install-mysql-on-centos-6))，记得设置字符为utf8mb4。在 `~/.my.cnf` 中设置：

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

如果遇到错误说 `"utf8mb4" charset is not compiled blabla...`, 打开`/usr/share/mysql/charsets/Index.xml` 在 `<charset name="utf8mb4">...</charset>` 后插入 [这段代码](https://www.zybuluo.com/xy0/note/509722)

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

7) 安装和运行Redis 

```shell
$ wget http://download.redis.io/releases/redis-2.8.3.tar.gz
$ tar xzvf redis-2.8.3.tar.gz
$ cd redis-2.8.3
$ make
$ make install
$ redis-server
```


# 部署nginx
前期先用nginx将域名www.mydomain.com转发到8001端口。

# 部署supervisor脚本
参考文件 `supervisord.conf`

# 部署crontab脚本
参考文件 `crontab`

# 系统使用文档


# API接口文档

