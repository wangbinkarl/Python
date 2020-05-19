#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose:  按mis1拆分fastq数据
# Author: Wangb
# Note:
# Last updated on: 2019-9-16
import gzip
import os
import re

def indexin(indexf):
#	读取index文件，将sample与P5,P7建立字典 
#	该文件格式为 
#	sampleid,p7,p5
	
	index_dict = {}
	for line in open(indexf,'r'):
		line = line.strip().split(',')
		sampleid = line[0]
		P57 = '+'.join(line[1:])
		index_dict[P57] = sampleid
	return index_dict

def mismatch_c(idx1,idx2,maxmis =1):
	'''
	两个index的P5，P7分别比对，错配默认为1
	返回1表示满足要求
	'''
	idx1 = idx1.split('+')
	idx2 = idx2.split('+')
	for i in range(2):
		mismatch = 0
		for n in range(len(idx1[i])):
			if idx1[i][n] != idx2[i][n]:
				mismatch += 1
		if mismatch > maxmis:
			return 0
	return 1

def match(indexdict,dir_dict,seq1,seq2):
#	R1,R2两条序列的index与目标index匹配，匹配上的则输出对应文件
	
	for idx in indexdict.keys():
		num = 0
		for seq in [seq1,seq2]:
			num +=1
			seq_index = seq[0].split(':')[-1]
			mismatch = mismatch_c(seq_index,idx)
			if mismatch==1:
				name = '%s_R%d.fastq' % (indexdict[idx],num)
				dir_dict[name].write('\n'.join(seq)+'\n')


#定义输入文件
index ='sample_index.txt'
test_R1 = 'test_R1.fastq.gz'
test_R2 = 'test_R2.fastq.gz'

indexdict = indexin(index)

#创建输出文件
dir_dict = {}
dirname = [value for value in indexdict.values()]
for name in dirname:                                #将需要生成的文件与该文件名建立字典
	nameR1 = '%s_R1.fastq' % name
	nameR2 = '%s_R2.fastq' % name
	file1 = open(nameR1,'w')
	file2 = open(nameR2,'w')
	dir_dict = dict({nameR1:file1,nameR2:file2},**dir_dict)	

#读取fastq数据
read1 = gzip.open(test_R1,'rt')
read2 = gzip.open(test_R2,'rt')

while True:　　　　　　　　　　　　　　　　　　　　　　＃遍历ｆａｓｔｑ，每次读四行
	seq1 = [read1.readline().strip() for i in range(4)]
	if not seq1:
    		break
	seq2 = [read2.readline().strip() for i in range(4)]
	match(indexdict, dir_dict, seq1, seq2)

for dir in dir_dict.keys():
	dir_dict[dir].close()
