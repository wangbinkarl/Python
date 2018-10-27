# -*- coding: UTF-8 -*-
#根据test1，在fastq中提取相关信息
aDict ={}
for line in open("C:/Python27/trainning/test1.fq"):
    if line[0] == '@':
        name = line.strip()[1:]
        #print name,
        aDict[name] = []
    else:
        aDict[name].append(line.strip())

for line in open("C:/Python27/trainning/fastq.name"):
    seq = line.strip()
    #print seq
    print "@%s\n%s" % (seq,'\n'.join(aDict[seq]))