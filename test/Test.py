from requests import request
from PIL import Image, ImageDraw, ImageFont
from lxml import etree

from paper import Paper, Img, Font

url = "https://zh.wikipedia.wikimirror.org/api/rest_v1/page/summary/"
header = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'}

word = '编译器'
res = request('get', url=url + word, headers=header).json()

tree = etree.HTML(res.get('extract_html'))
title = tree.xpath("//p/b/text()")[0]
content = res.get('extract')

wiki_logo = "./res/img/zhwiki-hans.png"
title_font = "./res/fonts/RHR/RHR-B.ttf"
content_font = "./res/fonts/RHR/RHR-R.ttf"

# 画板
sketchPad = Image.new('RGBA', (720, 1280), (255, 255, 255))
# 创建对象
wikiLogo = Image.open(wiki_logo)
titleFont = ImageFont.truetype(title_font, 28)
contentFont = ImageFont.truetype(content_font, 24)
imgDraw = ImageDraw.Draw(sketchPad)

# 绘图
# 粘贴wikiLogo
w, h = wikiLogo.size
_, _, _, a = wikiLogo.split()
# sketchPad.paste(wikiLogo, (36, 36), mask=a)
# 写字
# imgDraw.text((w + 36, 36), title, font=titleFont, fill=(12, 18, 24))
# imgDraw.text((w + 36, 36 + 36), content, font=contentFont, fill=(12, 18, 24))

ele = Img(wikiLogo)
elef = Font(titleFont, content)
for e in Paper().addFont(elef):
    imgDraw.text(*e, font=titleFont, fill=(12, 18, 24))
sketchPad.show()

# 4. 在图片上写字
# 第一个参数：指定文字区域的左上角在图片上的位置(x,y)
# 第二个参数：文字内容
# 第三个参数：字体
# 第四个参数：颜色RGB值
# img_draw.text((36, 36), chars, font=ttf, fill=(12, 18, 24))
#
# img_draw.text((36, 3*36), title, font=ttf, fill=(12, 18, 24))
#
# x, y = img.size
# r, g, b, a = img.split()
# for i in range(x):
#     for j in range(y):
#         color = list(img.getpixel((i, j)))
#         k = [bool(c) for c in color]
#         if not (k[0] and k[1] and k[2]):
#             color[:3] = [255, 255, 255]
#         img.putpixel((i, j), tuple(color))

# image.show()

# image.save("1.jpg")
