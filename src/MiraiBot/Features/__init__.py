"""
Features: 功能包
- 功能被拆分为单独的模块
"""
from .Image import Image
from .Ping import Ping


class Features:

    def __init__(self):
        self.Image = Image()
        self.Ping = Ping()

        self.manPage_ = f"""
Usage: :指令

:{self.Image.command}\t\t{self.Image.usage}
:{self.Ping.command}\t\t{self.Ping.usage}       
:zuan\t\t嘴臭一下
:help\t\t显示此列表

MultiCommand:
- 使用分隔符或者换行
- 分隔符:|,&,%

:指令[分割符]:指令
OR
:指令
:指令
"""

    def manPage(self):
        return 'text', self.manPage_
