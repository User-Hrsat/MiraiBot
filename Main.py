#! /usr/bin/env python3.8

import asyncio
import re

from graia.application.entry import (At, Friend, GraiaMiraiApplication, Group,
                                     Image, Member, MessageChain, Plain,
                                     Session, Xml)
from graia.broadcast import Broadcast

from Features import Feathures

app = Broadcast(loop=asyncio.get_event_loop())

mirai = GraiaMiraiApplication(
        broadcast = app,
        connect_info = Session(
            host = "http://127.0.0.1:8080",
            authKey = "MeuPasswd",
            account = 1291517893,
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

    switch = {                                      #switch/case
            'text' : Plain,                         #消息组件复用
            'image' : Image.fromFileSystem,         #消息组件复用
            'xml' : Xml,                            #消息组件复用
        }

    async def sendmessage(recall):
        try:
            remessage = recall[0]
            infotype = recall[1]
        except TypeError:
            return

        await mirai.sendGroupMessage(
                group.id,
                [
                    At(target=memberid),
                    switch[infotype](remessage)
                    ]
                )

    await sendmessage(Feathures(timestamp, membernames, memberid, messages))

if __name__ == "__main__":
    mirai.launch_blocking()
