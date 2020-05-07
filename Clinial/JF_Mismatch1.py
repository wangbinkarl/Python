#!/usr/bin/python
# -*- coding:utf-8 -*-
#Purpose:目的检查同条Lane中的index是否不一致的碱基数大于等于3，可用于mis1
#
import sys
from collections import defaultdict
from itertools import combinations

if len(sys.argv) < 2:
	print "Usage:\n     python {} Lane".format(sys.argv[0])
	exit(1)
def del_dict(p_dict):
	res_list = []
	for lane,lindex in p_dict.items():
		if lane != target_lane:
			continue
		'''对单个Lane中所有的index进行不重复的组合'''
		for index in combinations(lindex,2):
			res_list = [1 for i in range(len(index[0])) if index[0][i] != index[1][i]]
	
			if len(res_list) >= 3:
				continue
				#print 'Lane{}:index diff num >3'.format(lane)
			elif len(res_list) >0:
				print res_list,index
				print "Lane{}: diff num is {}".format(lane,len(res_list))
	print "It's over"

target_lane = sys.argv[1]
SS = 'SampleSheet_new.csv'
p75_dict = defaultdict(list)
with open(SS,'r') as f:
	for line in f:
		if line.startswith('Lane,Sample_ID'):
			break
	for line in f:
		num_lane = line.split(',')[0]
		p7 = line.split(',')[6]
		p5 = line.split(',')[8]		
		p75 = '{}{}'.format(p7,p5)
		p75_dict[num_lane].append(p75)

del_dict(p75_dict)
