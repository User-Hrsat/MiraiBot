class Paper:
    """
    固定宽度，无限长度的理想纸张
    默认长度1280，多退少补
    """

    def __init__(self, w=720, margin=36, linespacing=12):
        """
        默认设置(px)：
            宽度：720
            页边距：36
            行间距：12
        """
        self.w = w
        self.h = None
        self.h_ = []
        self.margin = margin
        self.linespacing = linespacing
        # 元素填充后剩下的空白块
        self.blank = []

    def layout(self, element):
        elements = None
        if isinstance(element, Img):
            self.addImg(element)
        if isinstance(element, Font):
            elements = self.addFont(element)
        self.h = self.h_[0]
        if elements:
            return elements

    def imglayout(self, img):
        self.h_.append(2*self.margin + img.size[-1])

    def fontLayout(self, font):
        x = self.w - self.margin * 2
        content = font.content
        size, counts = font.size

        # 每行的字数
        count = None
        for c in range(counts):
            # 宽度等于或稍微大于页面空白宽度的字符个数
            if (c + 1) * size >= x:
                count = c
                break

        # 整行
        lines = counts // count
        # 剩余字符
        residual = counts % count
        # lines 行数
        if residual:
            lines += 1

        # 分割字符串
        contents = []
        for i in range(lines):
            # 起始
            start = i * count
            # 结束
            end = (i + 1) * count
            # 剩余字符不足整行
            if end > counts:
                end = -1
            contents.append(content[start:end])

        # 坐标与文本内容
        fonts = []
        for i, c in enumerate(contents):
            position = (self.margin,
                        self.margin + (i * size) + (i * self.linespacing))

            fonts.append((position, c))

        self.h_.append(2*self.margin + lines * size + lines * self.linespacing)

        return fonts

    def addImg(self, img):
        return self.imglayout(img)

    def addFont(self, font):
        return self.fontLayout(font)


class Element:
    """
    基类：页面中的元素
    """
    def __init__(self, point):
        self.point = point
        self.size = None

    def __call__(self):
        return self, self.point, self.size


class Img(Element):
    def __init__(self, image, point=None):
        """
        img: 接收一个 PIL.Image 对象
        point: 接收一对 (x,y) 坐标值，作为左上角起始点；非必要
        """
        super().__init__(point)
        self.size = image.size


class Font(Element):
    def __init__(self, font, content, point=None):
        """
        img: 接收一个 PIL.ImageFont 对象
        point: 接收一对 (x,y) 坐标值，作为左上角起始点；非必要
        """
        super().__init__(point)
        self.content = content
        self.size = (font.size, len(self.content))

# 计算页面空白

# 固定布局和随机布局
