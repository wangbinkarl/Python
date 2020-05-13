##20200513
##该代码主要处理json格式文件，处理的目录是illumina Xten，Nova 仪器产生的数据目录
##从Json文件中获取该Lane的拆分明细，即每个样本产量，未拆出的产量及总量
#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose: 
# Author: Wangb
# Note:
# Last updated on: 2020-2-15
import sys
import json
from collections import defaultdict
import os
import subprocess
import glob
import argparse

mydict = {'sr':'BCLTMP_SR','cln':'BCLTMP','6-0':'RawData_6+0','8-0':'RawData_8+0','8+8':'RawData_8+8'}
def Json_del(Lane_json):
	with open(Lane_json) as f:
		myjson = json.load(f)
		for k in  myjson["ReadInfosForLanes"]:
			Lane = k["LaneNumber"]
		#各样本统计
		for i in myjson["ConversionResults"]:
			Sum_data = i['Yield']
			print('Lane total:{}G'.format(round(int(Sum_data)/1000/1000/1000.,2)))
			sample_total = 0
			for demux in i["DemuxResults"]:
				sid = demux["SampleId"].encode('utf-8')
				sample_sum = demux["Yield"]
				for sample in demux["IndexMetrics"]:
					index = sample["IndexSequence"].encode('utf-8')
				print('{} {}G {}'.format(sid,round(int(sample_sum)/1000/1000/1000.,2),index))
				sample_total += int(sample_sum)
			print('Dex: {}G'.format(round(int(sample_total)/1000/1000/1000.,2)))		
			undeter_sum =  i['Undetermined']["Yield"]
			print('Undeter: {}G'.format(round(int(undeter_sum)/1000/1000/1000.,2)))

if __name__ == '__main__':
	if len(sys.argv) <2:
		os.system("{} -h".format(sys.argv[0]))
		exit(0)
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--lane",help="lane number")
	parser.add_argument('-p', '--pattern', help='include:sr,cln,6-0,8-0,8+8')
	args = parser.parse_args()
	Lane_json = '{}/L00{}/Data/Intensities/BaseCalls/Stats/Stats.json'.format(mydict[args.pattern],args.lane)
	if os.path.exists(Lane_json):
		Json_del(Lane_json)
	else:
		print("Stats.json is not exists")
