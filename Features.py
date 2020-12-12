#! /usr/bin/env python3.8

import time
from copy import deepcopy
from os import popen
from random import randint
from re import match
from urllib import request

#import datetime
#import jieba                                           有点差劲唉,可能是没用好
#jieba.set_dictionary('./BadLanguage/dict.txt')
#jieba.load_userdict('./BadLanguage/badlanguage.txt')

class Clean:
    '''
    文本清洗
    适用于固定指令
    '''

    # comList: list = []                                这样写，内存泄漏了

    def __init__(self, messages):                       #清洗文本,去除换行、特殊符号以及去重

        self.messages = messages
        self.comList: list = []
        spwords = ('|', '&', '%')

        if match('^:', self.messages) == None:          #排除非特征信息,留做文本分析
            self.comList.append('analysis')
        else:
            for word in spwords:
                self.messages = self.messages.replace(word, '\n')  #去特殊字符
            self.comList = self.messages.splitlines()     #去换行

class Features:                                         #固定指令的功能

    def __init__(self, com):

        self.com = com

    def Card(self):

        return [('json', '{"app":"com.tencent.giftmall.giftark","desc":"","view":"giftArk","ver":"1.0.4.1","prompt":"[礼物]礼物","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"giftData":{"sender":"0","isFree":"1","giftName":"川建国","desc":"川建国已成为你的专属RBQ","orderNum":"","toUin":"","unopenIconUrl":"https:\/\/cdn.read.html5.qq.com\/image?src=circle&q=5&r=0&imgflag=7&cdn_cache=24&imageUrl=http%3A%2F%2Fp%2Eqpic%2Ecn%2Fmttcircle%2F0%2F51f9903584e80acdfm1721610i92183821%5F202010w04%5F80b935f111a4132a10e9ca3f4f0cc2e3%2Epn%2F0","openIconUrl":"https:\/\/cdn.read.html5.qq.com\/image?src=circle&q=5&r=0&imgflag=7&cdn_cache=24&imageUrl=http%3A%2F%2Fp%2Eqpic%2Ecn%2Fmttcircle%2F0%2F51f9903584e80acdfm1721610i92183821%5F202010w04%5F80b935f111a4132a10e9ca3f4f0cc2e3%2Epn%2F0","boxZipUrl":"","giftZipUrl":"","giftParticleUrl":"","msgId":""}},"config":{"forward":1},"text":"","sourceAd":"","extra":""}')]

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
        return [('image', "resource/images/zhwiki-hans.png"), ('text', "\n维基百科")]
    
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

class Analysis:
    '''
    语义分析
    后期需要接入redis使用词库实现图灵化
    包括Features里的函数
    '''

    mesdic : dict = {'init' : [['message', '#'], ['sender', '#']]}

    def __init__(self, sourceAll):

        self.timestamp, self.groupid, self.memberid, self.messages = sourceAll

    def Analysis(self):                                 #太差了
        '''
        勉强能用的上下文复读刷屏检测，不能检测跳跃式复读
        '''

        wlist = ('[图片]', '[表情]', '')

        if self.groupid not in self.mesdic:             #追加并初始化没有的群组
            self.mesdic[self.groupid] = [['messages', '#'], ['sender', '#']]

        # print("=====================")
        # print(f"始:=>{self.mesdic}")
        if len(self.mesdic[self.groupid][0]) < 3:       #列表仅有三项
            if self.messages not in wlist:              #排除无法检测的内容
                self.mesdic[self.groupid][0].append(self.messages)   #追加消息
                self.mesdic[self.groupid][1].append(self.memberid)   #追加发送者id
        
        if len(self.mesdic[self.groupid][0]) == 3:
            # print(f'中:=>{self.mesdic}')
            if self.mesdic[self.groupid][0][2] == self.mesdic[self.groupid][0][1]:
                self.mesdic[self.groupid][0].pop(0)
                if self.mesdic[self.groupid][1][2] == self.mesdic[self.groupid][1][1]:
                    self.mesdic[self.groupid][1].pop(0)
                    return '不要刷屏！'
                else:
                    self.mesdic[self.groupid][1].pop(0)
                    return '不许复读！'
            else:                                       #删除第一项
                self.mesdic[self.groupid][0].pop(0)
                self.mesdic[self.groupid][1].pop(0)
            # print(f"尾:=>{self.mesdic}")
            # print("=====================")

    def Run(self):
    #    timestamp = datetime.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
    #    date = {
    #            '时间' : timestamp,
    #            '昵称' : membernames,
    #            'ID' : memberid,
    #            '消息' : messages
    #            }                                      之前用结巴分词然后查txt太慢了，后续使用redis

        res = self.Analysis()
        if res:
            return [('text', res)]

        if self.messages == '检测':
            return [('text', '屑')]

class Proce:
    '''
    调度器
    所有功能的集中调度
    '''

    def __init__(self, sourceAll, com):
                                                        #是不是考虑一下元组拆包的特性以减少代码量
        self.sourceAll = sourceAll
        self.com = com

    def Run(self):

        switch = {
                ':网抑云' : Features.Cloudmusic,
                ':card' : Features.Card,
                ':image' : Features.Image,
                ':rss' : Features.RSS,
                ':zuan' : Features.Zuan,
                ':wiki' : Features.Wiki,
                ':help' : Features.Help
            }

        # print(f"self.com:=>{self.com}")

        try:
            if match('^:ping', self.com):               #特殊指令
                return Features(self.com).Ping()
            elif self.com == 'analysis':
                return Analysis(self.sourceAll).Run()
            else:
                return switch[self.com](self)
        except KeyError:
            return [('text', f"没有{self.com}这条命令!")]  
