"""
Features: 功能包
- 功能被拆分为单独的模块
"""
from .Image import Image
from .Ping import Ping

manPage_ = f"""
Usage: :指令
    
:{Image.command}\t\t{Image.usage}
:{Ping.command}\t\t{Ping.usage}       
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


class ManPage:
    def __call__(self):
        return manPage_
