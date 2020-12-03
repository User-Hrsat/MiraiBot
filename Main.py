#! /usr/bin/env python3.8

import asyncio

from graia.application.entry import (At, Friend, GraiaMiraiApplication, Group,
                                     Image, Json, Member, MessageChain, Plain,
                                     Session, Xml)
from graia.broadcast import Broadcast

from Features import Clean, Proce

app = Broadcast(loop=asyncio.get_event_loop())

mirai = GraiaMiraiApplication(
        broadcast = app,
        connect_info = Session(
            host = "http://127.0.0.1:8080",
            authKey = "INITKEYGMGZMdzU",
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
#async def subroutine0(mirai: Mirai):               #怎么拿message

@app.receiver("GroupMessage")
async def event_gm(mirai: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):

    messages = message.asDisplay()                  #消息
    timestamp = message.__root__[0].time            #每条消息的时间
    groupid = group.id                              #发消息的群/以免刷屏检测混淆
    memberid = member.id                            #发送消息的人

    sendmessages = MessageChain

    print(groupid)

    switch = {                                      #消息组件复用
            'text' : Plain,
            'image' : Image.fromLocalFile,
            'json' : Json,
            'xml' : Xml
        }

    async def sendmessage(remessage, infotype):     #没有考虑到多种类型的消息同时发送，需重写

        await mirai.sendGroupMessage(
                group.id,
                MessageChain(
                    __root__=[
                    At(target=memberid),
                    switch[infotype](remessage)
                    ]
                )
        )

    command = Clean(messages).Call()

    for com in command:

        try:
            recall = Proce(timestamp, groupid, memberid, messages, com).Run()
            await sendmessage(recall[0], recall[1])
            print(recall)
        except TypeError:
            return

if __name__ == "__main__":
    mirai.launch_blocking()
