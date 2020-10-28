#! /usr/bin/env python3

import datetime
import json
import os
import random
import re
import time
from urllib import request

#import jieba  # 有点差劲唉,可能是没用好
#jieba.set_dictionary('./BadLanguage/dict.txt')
#jieba.load_userdict('./BadLanguage/badlanguage.txt')

class Feathures():
 
    def __init__(self, timestamp: str, membernames: str, memberid: int, messages: str):
                                                                                #清洗文本,去除换行、特殊符号以及去重

        self.timestamp = timestamp
        self.membernames = membernames
        self.memberid = memberid
        self.messages = messages

        self.comms: list
        spew = ['|', '&', '%']
        switch = {
            ':网抑云' : self.Cloudmusic,
            ':image' : self.Image,
            ':rss' : self.RSS,
            ':zuan' : self.Zuan,
            ':help' : self.Help,
            'analysis': self.Analysis
            }

        if re.match('^:', self.messages) == None:                               #排除非特征信息,留做文本分析
            self.comms.append('analysis')
        else:
            for i in spew:
                self.comms = self.messages.replace(i, '\n')                     #去特殊字符
            self.comms = self.comms.splitlines()                                #去换行
            for i in self.comms:
                if re.match('^:', i) != None:                                   #保留以:开头的字段
                    if i == 'analysis':
                        switch[i](timestamp, membernames, memberid, messages)
                    elif re.match('^:ping', i):
                        self.Ping(i)
                    else:
                        switch[i]()

            #        self.comms.append(i)
            #self.comms = list(set(self.comms))          #去重

    def Analysis(self, timestamp, membernames, memberid, messages):
                                                        #文本分析
    #    timestamp = datetime.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
    #    date = {
    #            '时间' : timestamp,
    #            '昵称' : membernames,
    #            'ID' : memberid,
    #            '消息' : messages
    #            }
    #
    #    jsoncode = json.dumps(date)
    #    jsonfile = open('History.json', 'a+')
    #    jsonfile.write(jsoncode+'\n')
    #    jsonfile.close()                                #施工中...
    
    #    cutwords = jieba.lcut(messages)
    #    words = open('./BadLanguage/badlanguage.txt', 'r')
    #    for w in cutwords:
    #        if w+'\n' in words.readlines():
    #            words.close()
    #            return '不要讲脏话'
        if messages == '检测':
            return '屑', 'text'

    def Cloudmusic(self):
    
        return '正在施工', 'text'
    
    def Noncomd(self, i):                                     #不存在的指令
    
        if len(i) > 7:
            return
        else:
            return f"没有{i}这条命令!", 'text'
    
    def Image(self):
        num = random.randint(0, 2)
        return f"resource/images/{num}.jpg", 'image'
    
    def Ping(self, i: str):
        ip = re.match(":ping ((25[0-5])|(2[0-4]d)|(1dd)|([1-9]d)|d)(.((25[0-5])|(2[0-4]d)|(1dd)|([1-9]d)|d)){3}", i)
        url = re.match(":ping [a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?", i)
        
        if ip != None or url != None:
            resuatl = str()                             #预定义变量真不爽
            i = list(i)
            i.pop(0)                                    #去:号
            i = ''.join(i)                              #转换为字符串
            restr = os.popen(f"{i} -c 4")
            for i in restr.readlines():
                resuatl += i
            return resuatl, 'text'
    
        if ip == None and url == None:
            return """正确用法:
:ping IPor域名
一定要填写正确的IP或域名哦!""", 'text'
    
    def RSS(self):
        return '你说什么我听不懂', 'text'
    
    def Zuan(self):
        response = request.urlopen("https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn")
        zuan = response.read()
        return zuan.decode('utf-8'), 'text'
    
    def Help(self):                                         #明明我这边排版好好的
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
