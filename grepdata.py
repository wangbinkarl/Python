# -*- coding: UTF-8 -*-
#Date:2018-11-7
#Master Wang
#根据文件一的ID从文件二提取相应的信息并格式化输出

import sys

input_file1 = sys.argv[1]
input_file2 = sys.argv[2]
output_file = sys.argv[3]

aDict = {}
aList = []

for line in open(input_file1):
	id = line.strip()
	id2 = id.split()[0]
    #print id
	aDict[id2] = id

for data in open(input_file2):
	data1 = data.strip()
	id3 = data1.split()[0]
    #print id2
	if id3 in aDict:
		express = data1 + '\t' + aDict[id3]
		aList.append(express)
        #print data1
	else:
		continue
#aList.sort()
#print '\n'.join(aList)
#print '\n'.join(sorted(aList))
output = open(output_file,'w+')
output.write('\n'.join(sorted(aList)))