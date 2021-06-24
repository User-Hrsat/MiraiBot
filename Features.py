#! /usr/bin/env python3.9

#import time
from copy import deepcopy
from json import loads
from os import popen
from random import randint
from re import match
from urllib import parse, request

from requests import get

#import datetime
#import jieba                                           有点差劲唉,可能是没用好
#jieba.set_dictionary('./BadLanguage/dict.txt')
#jieba.load_userdict('./BadLanguage/badlanguage.txt')

class Features:                                         #固定指令的功能

    def __init__(self, com):

        self.com = com

    def Card(self):

        return [('json', {"app":"com.tencent.giftmall.giftark","desc":"","view":"giftArk","ver":"1.0.4.3","prompt":"1","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"giftData":{"animationType":"0","arkBgUrl":"\/qzone\/space_item\/material\/QzoneGift\/org\/12\/19676\/ke.png","arkGuestBgUrl":"\/qzone\/space_item\/material\/QzoneGift\/org\/13\/204973\/ke.png","boxZipUrl":"","desc":"","giftMsg":"（日期）","giftName":"时间:","giftParticleUrl":"\/aoi\/sola\/20200211152108_OwLVpEObQT.png","giftPrice":"6660","giftZipUrl":"\/qzone\/qzact\/act\/external\/shijun\/mghdh.zip","isFree":"0","lottieUrl":"","msgId":"6794593814080377150","openIconUrl":"\/aoi\/sola\/20200211152101_nl6z8Et70n.png","orderNum":"","sender":"1","toUin":"2012683191","unopenIconUrl":"\/aoi\/sola\/20190524114722_moYXoHozlK.png"}},"config":{"ctime":1581989650,"forward":0,"token":""}})]

    def Cloudmusic(self):
    
        return [('text', "正在施工")]

    def Image(self):
        num = randint(0, 2)
        return [('image', f"resource/images/{num}.jpg")]

    def Ping(self):
        #ip = match(r":ping ((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3}", self.com)
        url = match(r":ping [a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?", self.com)

        if url != None:
            resuatl: str = ""                           #预定义变量真不爽
            i = list(self.com)
            i.pop(0)                                    #去':'
            i = ''.join(i)                              #转换为字符串
            restr = popen(f"{i} -c 4")                  #调用系统
            for i in restr.readlines():
                resuatl += i
            return [('text', resuatl)]
    
        if url == None:
            return [('text', """
正确用法:
:ping IPor域名
一定要填写正确的IP或域名哦!""")]

    def RSS(self):
        return [('text', "你说什么我听不懂")]

    def Wiki(self):
        entry = self.com.split(' ')
        if len(entry) == 2:
            res = get(
                url=f"https://zh.wikipedia.wikimirror.org/api/rest_v1/page/summary/{entry[1]}",
                headers={
                    'accept-language' : 'zh-CN,zh;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
                })
            content = loads(res.text)
            #urllib的玩法
            #entry = parse.quote(entry[1], encoding='utf-8')
            #req = request.Request(
            #    url=f"https://zh.wikipedia.wikimirror.org/api/rest_v1/page/summary/{entry}",
            #    headers={
            #        'accept-language' : 'zh-CN,zh;q=0.9',
            #        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
            #    })
            #res = request.urlopen(req)
            #content = loads(res.read().decode('utf-8'))
            try:
                return [('image', "resource/images/zhwiki-hans.png"), ('text', f"\n============\n{content['extract']}")]
            except KeyError:
                return [('text', '什么都没有查到唉！\n可能没有这个条目或者指定条目名称错误！\n换一个试试吧:)')]
        else:
            return [('text', """
正确用法：
:wiki 条目名称
简体环境不够完善，可能导致查询无果！
还请见谅！！！""")]
    
    def Zuan(self):
        response = request.urlopen("https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn")
        zuan = response.read()
        return [('text', zuan.decode('utf-8'))]
    
    def Help(self):                                     #明明我这边排版好好的,辣稽
        return [('text', """
用法: :[指令]
    
:image      发送图片
:ping       就是ping嘛
:zuan       嘴臭一下
:help       显示此帮助列表

多命令用法:
    :[指令]分割符(|,&或%):[指令]
    OR
    :[指令]
    :[指令]""")]