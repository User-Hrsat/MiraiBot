from os import listdir
from random import choice


class Image:
    command = 'image'
    usage = '随机图片'

    def __init__(self):
        self.path_ = '../../res/img/'
        self.img_ = choice(listdir(self.path_))
        print('Image Init')

    def __call__(self):
        return 'img', f"{self.path_}{self.img_}"
