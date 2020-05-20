#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose: 转换照片为字符
# Author: Wangb
# Note:
# Last updated on: 2020-5-20
# version:python 3.7.4

from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()

imgpath = args.file
##
ascii_char = list(r"$@&%B#=-. ")

def select_ascii_char(r, g, b):
	gray = int((19595*r+38469*g+7472*b )>>16)
	unit = 256.0/len(ascii_char)
	return ascii_char[int(gray/unit)]

def output(imgpath,width=100,height=100):
	''' '''
	im = Image.open(imgpath)
	im = im.resize((width,height),Image.NEAREST)
	txt = ""

	for h in range(height):
		for w in range(width):
			txt += select_ascii_char(*im.getpixel((w,h))[:3])
		txt += '\n'
	return txt

def save_as_txtfile(txt):
	'''保存至文件'''
	with open('imgtochar.txt','w') as f:
		f.write(txt)

if __name__ == '__main__':
	print(output(imgpath,120,90))
	save_as_txtfile(output(imgpath,120,90))
