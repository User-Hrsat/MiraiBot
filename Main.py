#! /usr/bin/env python3.8

import asyncio
import re

from graia.application.entry import (At, Friend, GraiaMiraiApplication, Group,
                                     Image, Member, MessageChain, Plain,
                                     Session, Xml)
from graia.broadcast import Broadcast

import Features

app = Broadcast(loop=asyncio.get_event_loop())

mirai = GraiaMiraiApplication(
        broadcast = app,
        connect_info = Session(
            host = "http://127.0.0.1:8080",
            authKey = "",
            account = 123,
            websocket = True
        )
)

#authKey = ""
#qq = 

#mirai = Mirai(f"mirai://127.0.0.1:8080/?authKey={authKey}&qq={qq}", websocket=True)

#@mirai.onStage("around")                           #脚本启动或关闭时给我发消息
#async def greet(mirai: Mirai):

#@mirai.subroutine
#async def subroutine0(mirai: Mirai):                #怎么拿message

@app.receiver("GroupMessage")
async def event_gm(mirai: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):

    messages = message.toString()                   #留做刷屏和脏话的检测
    timestamp = message.__root__[0].time            #每条消息的时间
    membernames = member.memberName
    memberid = member.id                            #发送消息的人

    command = Features.Clear(messages)              #清洗文本,提取指令

#    Features.Analysis(timestamp, membernames, memberid, messages)
                                                    #文本分析:刷屏、脏话、复读机

#    global mesarr
#    if len(mesarr) <= 3:
#        mesarr.append(messages)
#        print(mesarr)
#    if len(mesarr) == 3:
#        if mesarr[2] == mesarr[1]:
#            await mirai.sendGroupMessage(
#                    group.id,
#                    [
#                        Plain(text='匹配')
#                        ]
#                    )
#        mesarr.pop(0)

    switch = {                                      #switch/case
            'text' : Plain,                         #消息组件复用
            'image' : Image.fromFileSystem,         #消息组件复用
            'xml' : Xml,                     #消息组件复用
            ':网抑云' : Features.Cloudmusic,
            ':image' : Features.Image,
            ':rss' : Features.RSS,
            ':zuan' : Features.Zuan,
            ':help' : Features.Help,
            'analysis': Features.Analysis
        }

    async def sendmessage(i):

        try:
            if i == 'analysis':
                try:
                    getmessages, infotype = switch[i](timestamp, membernames, memberid, messages)
                except TypeError:
                    return
            else:
                getmessages, infotype = switch[i]()
        except KeyError:                            #需要参数或者匹配的
            if re.match('^:ping', i):
                getmessages, infotype = Features.Ping(i)
            else:
                return

        await mirai.sendGroupMessage(
                group.id,
                [
                    At(target=memberid),
                    switch[infotype](getmessages)
                    ]
                )

    for i in command:                               #经过清洗提取的指令会逐一运行
        await sendmessage(i)

if __name__ == "__main__":
    mirai.launch_blocking()
