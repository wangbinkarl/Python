#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose: 
# Author: Wangb
# Note:
# Last updated on: 2020-04-04
#输入文件格式：
#1_PA202J0002-C5C7AA7XKF1-A001L000
#1_PA2002190001DP01
#下游脚本是depth_GC_plot.r
import sys
import os
import gzip
from collections import defaultdict

def exact_depth(depth_file):
	mydictx = {} 
	with gzip.open(depth_file, 'rt') as depth:
	#with open(depth_file, 'r') as depth:
		header = next(depth)
		for line in depth:
			line = line.strip()
			chrx,start,end,avgdepth,_,_,_ = line.split()
			index = '{}:{}-{}'.format(chrx,start,end)
			if fadict.has_key(index):
				mydictx["{}\t{}\t{}".format(chrx,start,end)] = "{}\t{}".format(avgdepth,fadict[index])
	return mydictx

def info_exact(info_file):
	Xdict={};Mdict={}
	with open(info_file,'r') as f:
		for line in f:
			line = line.strip()
			Xtenid,Mgiid,panel,Lane,source = line.split()	
			if panel == "Goliath.cfg":
				fafile = "Bed/Goliath.fa"
			elif panel == "LungH4K.cfg":
				fafile = "Bed/LungH4K.fa"
			Xdict[Xtenid] = 'Xtentsv {}'.format(fafile)
			Mdict[Mgiid] = 'Mgitsv {}'.format(fafile)
	return Xdict,Mdict

info_file = "panel_sample.source.Lanex.list"
Xdict,Mdict = info_exact(info_file)

rawid = sys.argv[1]
sampleid = rawid.split('_')[1]
if Xdict.has_key(sampleid):
	fa_file = '{}'.format(Xdict[sampleid].split()[1])
	depth_file = '{}/{}.region.tsv.gz'.format(Xdict[sampleid].split()[0],sampleid)
elif Mdict.has_key(sampleid):
	fa_file = '{}'.format(Mdict[sampleid].split()[1])
	depth_file = '{}/{}.region.tsv.gz'.format(Mdict[sampleid].split()[0],sampleid)

fa_fileOpen = open(fa_file,'r')

fadict = {}

while True:
	#read1,read2每次读取四行
	read1 = [fa_fileOpen.readline().strip() for i in range(2)]
	if not read1[0]:
		break
	site = read1[0].split('>')[1]
	seq = read1[1]
	A_content = round(int(seq.count('A'))*1./len(seq),2)
	T_content = round(int(seq.count('T'))*1./len(seq),2)
	C_content = round(int(seq.count('C'))*1./len(seq),2)
	G_content = round(int(seq.count('G'))*1./len(seq),2)
	
	GC = round( (int(seq.count('G') ) + int( seq.count('C') ) ) *1./len(seq),2)
	
	fadict[site] = '{}\t{}\t{}\t{}\t{}'.format(GC,A_content,T_content,G_content,C_content)


depth_dict = exact_depth(depth_file)

OUT = open("{}.csv".format(rawid),'w')
OUT.write("seq_ID\tseq_start\tseq_end\tdepth\tGC\tA\tT\tG\tC\n")
for flag,value in sorted(depth_dict.items(),key=lambda depth_dict:(depth_dict[0].split()[0],depth_dict[0].split()[1])):
	OUT.write("{}\t{}\n".format(flag,value))

fa_fileOpen.close()
OUT.close()
