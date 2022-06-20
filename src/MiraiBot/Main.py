#! /usr/bin/env python

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config, WebsocketClientConfig
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend, Group
from graia.broadcast import Broadcast
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

from Handler import Handler

# 处理器
handler = Handler()

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
    # 对象方法
    config(
        # 账号
        1234567890,
        # 校验码
        "verifyKey",
        # HttpAPI服务的地址
        # HttpClientConfig("http://ip:port"),
        # 只能二选一
        # WebSocket地址
        WebsocketClientConfig("http://ip:port")
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
async def schedule():
    ...


@bcc.receiver("GroupMessage")
async def groupMessageListener(group: Group, message: MessageChain):
    await messageSender(group, handler(message.display))


@bcc.receiver("FriendMessage")
async def friendMessageListener(friend: Friend, message: MessageChain):
    await messageSender(friend, handler(message.display))


async def messageSender(rec, content):
    await app.sendMessage(rec, content)


if __name__ == "__main__":
    app.launch_blocking()
