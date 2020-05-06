#!/usr/bin/python
# -*- coding:utf-8 -*-
#Purpose:判断下机数据fastq与SS中是否一致，一致则提交JF_miseq_bcl...
#
import os
import sys
import argparse

def SS_del(SS):
	'''返回SampleSheet中所有样本id的list'''
	slist = []
	with open(SS,'r') as f:
		for line in f:
			if line.startswith('Sample_ID'):
				break
		for line in f:
			sampleid = line.strip().split(',')[0]
			slist.append(sampleid)
	return slist

def fc_del(fc,sr_project):
	fc_dir = os.path.join("/GPFS07/SequencingData7",fc)
	rawdata_dir = os.path.join(fc_dir,'Data/Intensities/BaseCalls/')
	SS = os.path.join(fc_dir,'SampleSheet_new.csv')
	if not os.path.exists(SS):
		SS = os.path.join(fc_dir,'SampleSheet.csv')

	SS_list = SS_del(SS)
	sample_count = len(SS_list)
	sample_count2 = sample_count*2
	idx_list = []
	'''获取拆分完的所有fastq文件，并保存至列表'''
	for i in os.listdir(rawdata_dir):
		if i.endswith('gz'):
			idx = i.split('_')[0]
			idx_list.append(idx)

	fastq_count = len(idx_list)
	idx_new =  set(idx_list)
	'''比较列表,集合运算'''
	diff = list(set(SS_list)-idx_new)
	new_diff = list(diff)
	print 'fastq length is:{}; SampleSheet sample id is:{} '.format(fastq_count,sample_count)
	if not diff and fastq_count == sample_count2:
		print 'Check Sucess\n'
		os.chdir(fc_dir)
		print os.getcwd()
		cmd = 'nohup JF_miseq_bcl2fq_withSync.py -n {} -f {}  &'.format(sr_project,fc)
		#os.system(cmd)
	elif not diff:
		print 'There are not exists R1 or R2\n'
	else:
		
		print 'There are not exists:{}\n'.format(','.join(new_diff))

if __name__ == '__main__':
	if len(sys.argv)==1:
		sys.argv.append('-h')

	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--sr_name",help="sr project name[such as SR18289]")
	parser.add_argument('-f', '--flowcell', help='sequence folder name')
	args = parser.parse_args()

	sr_project = args.sr_name
	fcs = args.flowcell
	for fc in fcs.split(','):
		#print fc
		fc_del(fc,sr_project)
