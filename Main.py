#! /usr/bin/env python3.8

import asyncio

from graia.application.entry import (At, Friend, GraiaMiraiApplication, Group,
                                     Image, Member, MessageChain, Plain,
                                     Session, Xml)
from graia.broadcast import Broadcast

from Features import Clean, Proce

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
#async def subroutine0(mirai: Mirai):               #怎么拿message

@app.receiver("GroupMessage")
async def event_gm(mirai: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):

    messages = message.asDisplay()                  #消息
    timestamp = message.__root__[0].time            #每条消息的时间
    membernames = member.name
    memberid = member.id                            #发送消息的人

    switch = {                                      #消息组件复用
            'text' : Plain,
            'image' : Image.fromLocalFile,
            'xml' : Xml
        }

    async def sendmessage(remessage, infotype):

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

        recall = Proce(timestamp, membernames, memberid, messages, com).Run()
        print(recall)
        await sendmessage(recall[0], recall[1])

if __name__ == "__main__":
    mirai.launch_blocking()
