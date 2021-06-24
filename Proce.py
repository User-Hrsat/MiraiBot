import Features
from re import match
from Analysis import Analysis

class Proce:
    '''
    调度器
    所有功能的集中调度
    '''

    def __init__(self, sourceAll, com):

        self.sourceAll = sourceAll
        self.com = com

    def Run(self):

        switch = {
                ':网抑云' : Features.Cloudmusic,
                ':card' : Features.Card,
                ':image' : Features.Image,
                ':rss' : Features.RSS,
                ':zuan' : Features.Zuan,
                ':help' : Features.Help
            }

        # print(f"self.com:=>{self.com}")

        if match('^:ping', self.com):                   #特殊指令
            return Features(self.com).Ping()
        elif match('^:wiki', self.com):                 #已凸显局限性，需改进
            return Features(self.com).Wiki()
        elif self.com == 'analysis':
            return Analysis(self.sourceAll).Run()
        else:
            try:
                return switch[self.com](self)
            except KeyError:
                return [('text', f"没有{self.com}这条命令!")]  