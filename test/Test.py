#! /usr/bin/env python3.8

import asyncio

from graia.application.entry import (At, Friend, GraiaMiraiApplication, Group,
                                     Image, Json, Member, MessageChain, Plain,
                                     Session, Xml)
from graia.broadcast import Broadcast

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

@app.receiver("GroupMessage")
async def event_gm(mirai: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    print(f"{mirai}\n{message}\n{group}\n{member}")

if __name__=="__main__":
    mirai.launch_blocking()
