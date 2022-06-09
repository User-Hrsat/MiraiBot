#! /usr/bin/env python

import asyncio

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config, HttpClientConfig, WebsocketClientConfig
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, Group
from graia.broadcast import Broadcast
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

# loop = asyncio.new_event_loop()
# Broadcast的__init__给过了new_event_loop()
bcc = Broadcast()

# 定时任务
scheduler = GraiaScheduler(loop=bcc.loop, broadcast=bcc)

# 类方法，和scheduler共用一套loop和bcc
# 可以让scheduler与Ariande一起跑
# 不设置的话Ariadne会自己生成一套
Ariadne.config(loop=bcc.loop, broadcast=bcc)
app = Ariadne(
    config(
        123456789,                                              # 机器人的QQ号
        "verifyKey",                                            # verifyKey
        HttpClientConfig("http://ip:4201"),                    # HttpAPI服务的地址
        WebsocketClientConfig("http://ip:4202")                 # WebSocket地址
    )
)

# crontabify()设置时间
# *    *    *    *    *    *
# -    -    -    -    -    -
# |    |    |    |    |    + 秒 (0-59) (可有可无吧，应该)
# |    |    |    |    +----- 星期中星期几 (0 - 6) (星期天 为0)
# |    |    |    +---------- 月份 (1 - 12)
# |    |    +--------------- 一个月中的第几天 (1 - 31)
# |    +-------------------- 小时 (0 - 23)
# +------------------------- 分钟 (0 - 59)
@scheduler.schedule(crontabify('12 20 * * * 24'))
async def maid():
    ...

@bcc.receiver("GroupMessage")
async def groupMessageListener(group: Group, message: MessageChain):
    ...

@bcc.receiver("FriendMessage")
async def friendMessageListener(friend: Friend, message: MessageChain):
    ...

async def messageSender(id, message):
    if message.asDisplay() == "123":
        await app.sendMessage(id, MessageChain.create([
            Plain("OK")
        ]))

if __name__ == "__main__":
    app.launch_blocking()