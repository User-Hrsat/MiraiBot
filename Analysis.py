class Analysis:
    '''
    语义分析
    后期需要接入redis使用词库实现图灵化
    包括Features里的函数
    '''

    mesdic : dict = {'init' : [['message', '#'], ['sender', '#']]}

    def __init__(self, sourceAll):

        self.timestamp, self.groupid, self.memberid, self.messages = sourceAll

    def Analysis(self):                                 #太差了
        '''
        勉强能用的上下文复读刷屏检测，不能检测跳跃式复读
        '''

        wlist = ('[图片]', '[表情]', '')

        if self.groupid not in self.mesdic:             #追加并初始化没有的群组
            self.mesdic[self.groupid] = [['messages', '#'], ['sender', '#']]

        # print("=====================")
        # print(f"始:=>{self.mesdic}")
        if len(self.mesdic[self.groupid][0]) < 3:       #列表仅有三项
            if self.messages not in wlist:              #排除无法检测的内容
                self.mesdic[self.groupid][0].append(self.messages)   #追加消息
                self.mesdic[self.groupid][1].append(self.memberid)   #追加发送者id
        
        if len(self.mesdic[self.groupid][0]) == 3:
            # print(f'中:=>{self.mesdic}')
            if self.mesdic[self.groupid][0][2] == self.mesdic[self.groupid][0][1]:
                self.mesdic[self.groupid][0].pop(0)
                if self.mesdic[self.groupid][1][2] == self.mesdic[self.groupid][1][1]:
                    self.mesdic[self.groupid][1].pop(0)
                    return '不要刷屏！'
                else:
                    self.mesdic[self.groupid][1].pop(0)
                    return '不许复读！'
            else:                                       #删除第一项
                self.mesdic[self.groupid][0].pop(0)
                self.mesdic[self.groupid][1].pop(0)
            # print(f"尾:=>{self.mesdic}")
            # print("=====================")

    def Run(self):
    #    timestamp = datetime.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
    #    date = {
    #            '时间' : timestamp,
    #            '昵称' : membernames,
    #            'ID' : memberid,
    #            '消息' : messages
    #            }                                      之前用结巴分词然后查txt太慢了，后续使用redis

        switch = {
                '歪比歪比' : "歪比巴卜",
                '歪比巴卜' : "歪比歪比"
            }
        res = self.Analysis()
        if res:
            return [('text', res)]
        else:
            try:
                return [('text', switch[self.messages])]
            except KeyError:
                return