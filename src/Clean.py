from re import match

class Clean:
    '''
    文本清洗
    适用于固定指令
    '''

    # comList: list = []                                这样写，内存泄漏了

    def __init__(self, messages):                       #清洗文本,去除换行、特殊符号以及去重

        self.messages = messages
        self.comList: list = []
        spwords = ('|', '&', '%')

        if match('^:', self.messages) == None:          #排除非特征信息,留做文本分析
            self.comList.append('analysis')
        else:
            for word in spwords:
                self.messages = self.messages.replace(word, '\n')  #去特殊字符
            self.comList = set(self.messages.splitlines())     #去换行,去重