from PIL import Image, ImageDraw, ImageFont
from paper import Paper, Img, Font


wiki_logo = "./res/img/zhwiki-hans.png"
content = "编译器（compiler）是一种电脑程式，它会将某种程式语言写成的原始码（原始语言）转换成另一种程式语言（目标语言）。"
title_font = "./res/fonts/RHR/RHR-B.ttf"
content_font = "./res/fonts/RHR/RHR-R.ttf"

wikiLogo = Image.open(wiki_logo)
titleFont = ImageFont.truetype(title_font, 28)
contentFont = ImageFont.truetype(content_font, 24)

_, _, _, a = wikiLogo.split()

paper = Paper()
img = Img(wikiLogo)
font = Font(contentFont, content)
paper.layout(img)
element = paper.layout(font)

sketchPad = Image.new('RGBA', (paper.w, paper.h), (255, 255, 255))
imgDraw = ImageDraw.Draw(sketchPad)

sketchPad.paste(wikiLogo, (paper.margin, paper.margin), mask=a)

for e in element:
    imgDraw.text(*e, font=contentFont, fill=(12, 18, 24))
sketchPad.show()

# sketchPad.save("C:/Users/Lilim/Desktop/123.png", format='png')

