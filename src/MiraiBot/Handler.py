from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Face, Image, Plain, Quote

from Clean import Clean
from Features import Features


class Handler:
    def __init__(self):
        # Todo
        # 可有用Ariadne的输出
        print('Handler Init')
        self.clean = Clean()
        self.features = Features()

        # 功能路由
        self.featureMap = {
            f':{self.features.Image.command}': self.features.Image,
            f':{self.features.Ping.command}': self.features.Ping,
            ':help': self.features.manPage
        }

        # 消息元素
        self.elementMap = {
            'at': At,
            'emoji': Face,
            'img': Image,
            'text': Plain,
            'quote': Quote
        }

    def messageCreater(self, results):
        # 对象的生命周期笔方法长
        # 用局部变量不要用对象属性
        content = MessageChain(Plain(''))

        for res in results:
            target, source = res
            element = self.elementMap.get(target)
            # 生成消息元素并追加到消息链
            content.append(element(source))
        return content

    def waiter(self, message):
        # 处理结果
        results = []

        # 可用的命令
        avail = self.featureMap.keys()
        # 清洗并剔除不存在的命令
        commands = [c for c in self.clean(message) if c[0] in avail]
        # 区分有无参数，长度大于1的有参数
        boolean = [len(c) > 1 for c in commands]

        for k, c in zip(boolean, commands):
            action = self.featureMap.get(c[0])
            if k:
                # 命令的参数
                results.append(action(c[1:]))
            else:
                results.append(action())
        return results

    def __call__(self, message):
        return self.messageCreater(self.waiter(message))
