import Features
from Clean import Clean


class Handler:
    def __init__(self):
        self.clean = Clean()

        self.router = {                                     # 功能路由
            f':{Features.Image.command}': Features.Image(),
            f':{Features.Ping.command}': Features.Ping(),
            ':help': Features.ManPage()
        }

    def __call__(self, commands):
        results = []                                        # 处理结果
        avail = self.router.keys()
        commands = [c for c in commands if c[0] in avail]   # 可用的指令
        boolean = [len(c) > 1 for c in commands]            # 区分有无参数
        for k, c in zip(boolean, commands):
            action = self.router.get(c[0])
            if k:
                c = c[1:]
                # Todo
                # 参数的个数 需要一个更优雅的方案
                if len(c) <= 1:
                    c = c[0]
                results.append(action(c))
            else:
                results.append(action())
        return results
