from re import match


class Clean:
    """
    文本清洗
    适用于固定指令
    """
    spwords = ('|', '&', '%')

    def __init__(self):  # 清洗文本,去除换行、特殊符号以及去重
        self.commands = []

    def __call__(self, message):
        if match('^:', message):  # 以:来头
            for word in self.spwords:
                message = message.replace(word, '\n')  # 替换特殊字符
            message = message.splitlines()  # 去换行

        for line in message:
            line = (line.split(' '))
            if line not in self.commands:
                self.commands.append(line)
            else:
                continue

        return self.commands
