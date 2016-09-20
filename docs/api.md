接口文档
==========

# 添加/修改公众号
功能: 输入需要爬取的公众号id和爬取频率,如果公众号不存在就添加,如果已经存在就更新爬取频率.同事更新公众号信息.包括头像,描述,二维码等.

URL: http://127.0.0.1:8090/api/wechat/add/

方法: POST

参数:
```
wechatid: 微信id
frequency:  爬取频率, 正整数, 单位是分钟
```
返回:
```
// 已存在更新返回
{
    "message": "已更新",
    "ret": 0
}
// 不存在保存后返回
{
    "message": "已添加",
    "ret": 0
}
// 没有找到对应的微信id
{
    "message": "公众号不存在",
    "ret": 1
}
```


# 添加文章

功能: 输入需要爬取的文章URL.将文章加入爬取队列优先爬取.同事获取相关公众号信息,并将爬取频率设置为0

URL: http://127.0.0.1:8090/api/wechat/topic/add/

方法: POST

参数: 
```
url: 文章连接,如http://mp.weixin.qq.com/s?__biz=MjM5NDg2NjA4MQ==&mid=402566965&idx=1&sn=616fb1ffa9afc5acc3f4f2a210f6dd83&3rd=MzA3MDU4NTYzMw==&scene=6#rd
```

返回:
```
// 正确返回
{
    'ret': 0,
    'message': '提交成功,链接已经提交给爬虫,稍后查看爬取结果'
}

// 错误返回
{
    'ret': 1,
    'message': '提交失败,url必须以 http://mp.weixin.qq.com/ 开头'
}
```




# 搜索api

功能: 输入公众号名称或者id,返回对应的列表.

URL: http://127.0.0.1:8090/api/wechat/search?query=财经

方法: GET

返回:

```
 {
    "data": [
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/h3VIR0DEFX5qh1EknyCj",
            "wechatid": "LLDS365",
            "intro": "本号出租/出售.关注后,即可进入【财经论坛】,和大家互动交流! 专注分享最实用的财经消息以及股票内容!欢迎关注!合作QQ800178778",
            "name": "財經",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt3HcMp751wj8bt3PNRmRzHg"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/vklgb27EEFBvh38Mnxya",
            "wechatid": "zdbank",
            "intro": "指点财经每日提供全面真实的财经快讯,发布最新银行理财、保险、资管、信托等正规金融机构发布的产品信息并高效对接理财师,成为投资者一站式理财资讯交互平台.",
            "name": "指点财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt-wxZs0pb4AGlpIKntt-xxo"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/MHVmaV-EomHdh04KnyAU",
            "wechatid": "cctvyscj",
            "intro": "中央电视台",
            "name": "央视财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt_cUwbglodLkLT749ZABOt4"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/dUOmqSDE0R6uhzHKnxZR",
            "wechatid": "tttmoney",
            "intro": "原创的财经评论,独立的观察视角,深度的市场剖析. 联系方式:QQ:1527356260;邮箱:1527356260@qq.com.",
            "name": "博闻财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFtza9DUiaCPSyfc_MQO4N5PY"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/H0jT3OvEsNXPh-q-nx07",
            "wechatid": "lianhuacaijing",
            "intro": "莲花APP官微,让你的财富在这里绽放.依托证券时报22年资本市场专业背景,抢先知晓上市公司公告解读、热点事件分析、主题机会挖掘;更有上市公司深度研究及最新机构调研动向.",
            "name": "莲花财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFtxNDf-e3-9SNoKmaZ8B9hcw"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/5XVNQmXEd1sIh3QhnyDB",
            "wechatid": "sohucaijing2013",
            "intro": "搜狐财经,不海量,不枯燥,财经可以很简单!这里有最及时资讯、最独家爆料、最麻辣点评,最权威的专家学者声音.",
            "name": "搜狐财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt89mqsRNr-HSk72nHeLEUls"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/D0wGCVjEpGbbh0lqnxkr",
            "wechatid": "bxcjtv",
            "intro": "百姓财经栏目是四川广播电视台经济频道2007年强力推出的一档财经类节目.从百姓投资理财的需求出发,以中国股市为着眼点,联手全国一流券商、邀请资深专业人士,以超前的眼光、敏锐的视角、权威的分析、把握大势,...",
            "name": "百姓财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFtzfSD2HictGHcf_wip7ImVU"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/tkP59tLEEuxth8OVnxaS",
            "wechatid": "njue_xcb_weixin",
            "intro": "南京财经大学官方公众平台,传播校园文化,传递校园信息,服务广大师生校友.欢迎关注!",
            "name": "南京财经大学",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt2H_o--VPZokXgl-56Mhh1g"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/UUgYF4fE-rmBh5Z0nx11",
            "wechatid": "bh2056",
            "intro": "做有趣、有料、有新意的大众金融平台",
            "name": "渤海财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFtyo_x125073RKHO4j27ZEtE"
        },
        {
            "qrcode": "http://img03.sogoucdn.com/app/a/100520105/7HVuYcHEfv8Bh9ACnyDI",
            "wechatid": "wzdsbcf",
            "intro": "欢迎关注温州财经,本公众号由温州都市报财经部运营,为广大温都爱理财俱乐部成员提供在线搜索、便民服务、财经新闻,以及在线股票问诊、国企类理财产品服务.",
            "name": "温州财经",
            "avatar": "http://img01.sogoucdn.com/app/a/100520090/oIWsFt0G2xPqCn-pG1sAAY2n8GI4"
        }
    ],
    "ret": 0
}
```