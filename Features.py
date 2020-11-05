#! /usr/bin/env python3

import time
from os import popen
from random import randint
from re import match
from urllib import request

#import datetime
#import jieba  # 有点差劲唉,可能是没用好
#jieba.set_dictionary('./BadLanguage/dict.txt')
#jieba.load_userdict('./BadLanguage/badlanguage.txt')

class Clean():

    def __init__(self, messages):                                               #清洗文本,去除换行、特殊符号以及去重

        self.messages = messages

        self.comms: list = []
        spew = ['|', '&', '%']

        if match('^:', self.messages) == None:                                  #排除非特征信息,留做文本分析
            self.comms.append('analysis')
        else:
            for i in spew:
                self.messages = self.messages.replace(i, '\n')                  #去特殊字符
            self.comms = self.messages.splitlines()                             #去换行

    def Clean(self):
        print(self.comms)
        return self.comms

class Features():

    def __init__(self, com):

        self.com = com

    def Cloudmusic(self):
    
        return '正在施工', 'text'

    def Image(self):
        num = randint(0, 2)
        return f"resource/images/{num}.jpg", 'image'

    def Noncomd(self):                                                          #不存在的指令

        if len(self.com) > 7:
            return
        else:
            return f"没有{self.com}这条命令!", 'text'

    def Ping(self):
        #ip = match(r":ping ((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3}", self.com)
        url = match(r":ping [a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?", self.com)

        if url != None:
            resuatl: str = ''                                                   #预定义变量真不爽
            i = list(self.com)
            i.pop(0)                                                            #去':'
            i = ''.join(i)                                                      #转换为字符串
            restr = popen(f"{i} -c 4")                                          #调用系统
            for i in restr.readlines():
                resuatl += i
            return resuatl, 'text'
    
        if url == None:
            return """正确用法:
:ping IPor域名
一定要填写正确的IP或域名哦!""", 'text'

    def RSS(self):
        return '你说什么我听不懂', 'text'
    
    def Zuan(self):
        response = request.urlopen("https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn")
        zuan = response.read()
        return zuan.decode('utf-8'), 'text'
    
    def Help(self):                                                             #明明我这边排版好好的
        return """用法: :[指令]
    
:image      发送图片
:ping       就是ping嘛
:zuan       嘴臭一下
:help       显示此帮助列表

多命令用法:
    :[指令]分割符(|,&或%):[指令]
    OR
    :[指令]
    :[指令]""", 'text'

class Analysis():                                                               #语义分析，图灵化

    def __init__(self, timestamp, membernames, memberid, messages):

        self.timestamp = timestamp
        self.membernames = membernames
        self.memberid = memberid
        self.messages = messages

    def Run(self):
    #    timestamp = datetime.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
    #    date = {
    #            '时间' : timestamp,
    #            '昵称' : membernames,
    #            'ID' : memberid,
    #            '消息' : messages
    #            }                                                              之前用结巴分词然后查txt太慢了，后续使用redis

        if self.messages == '检测':
            return '屑', 'text'

class Proce():                                                                  #路由

    def __init__(self, timestamp, membernames, memberid, messages, com):

        self.timestamp = timestamp
        self.membernames = membernames
        self.memberid = memberid
        self.messages = messages
        self.com = com

    def Run(self):

        switch = {
           ':网抑云' : Features.Cloudmusic,
           ':image' : Features.Image,
           ':rss' : Features.RSS,
           ':zuan' : Features.Zuan,
           ':help' : Features.Help
           }

        try:
            if match('^:ping', self.com):                                       #特殊指令
                return Features(self.com).Ping()
            elif self.com == 'analysis':
                return Analysis(self.timestamp, self.membernames, self.memberid, self.messages).Run()
            else:
                return switch[self.com](self)                                   #处理结果以及类型
        except KeyError:
            Features(self.com).Noncomd()
