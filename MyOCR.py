# -*- coding: utf-8 -*-
# @Date    : 2017/2/1
# @Author  : hrwhisper

import os
import re


def image_to_string(img, cleanup=True):
    # cleanup为True则识别完成后删除生成的文本文件
    # tesseract a.png result
    os.system('tesseract ' + img + ' ' + img)  # 生成同名txt文件F
    with open(img + '.txt') as f:
        t = f.read()
        text, _ = re.subn('[\W]', '', t) if t else ('', '')
    if cleanup:
        os.remove(img + '.txt')
    return text
