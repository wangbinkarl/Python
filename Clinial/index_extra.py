#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose:  根据index提取数据 检查个数
# Author: Wangb
# Note:
# Last updated on: 20- -
import sys
import os

def extra(file2):
	with open(file2,'r') as f:
		for line in f:
			line = line.strip()
			infox = line.split(',')[0]
			if mydict.has_key(infox):
				print line

def info(file1):
	mydict={}
	with open(file1,'r') as f:
		header = next(f)
		for line in f:
			line = line.strip()
			mydict[line] = 1
	return mydict

file_info = sys.argv[1]
info_csv = sys.argv[2]

mydict = info(file_info)

extra(info_csv)
