from re import match


class Clean:
    """
    文本清洗
    适用于固定指令
    """
    spwords = ('|', '&', '%')

    def __init__(self):
        ...

    # 清洗文本,去除换行、特殊符号以及去重
    def __call__(self, message):
        # 对象的生命周期笔方法长
        # 用局部变量不要用对象属性
        commands = []
        # 以:开头
        if match('^:', message):
            for word in self.spwords:
                # 替换特殊字符
                message = message.replace(word, '\n')
            # 去掉换行
            message = message.splitlines()

        for line in message:
            # 用空格拆分命令和参数
            line = (line.split(' '))
            if line not in commands:
                commands.append(line)

        return commands

    def __del__(self):
        ...
