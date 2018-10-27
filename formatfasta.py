# -*- coding: UTF-8 -*-
##对fasta格式的序列指定行长度
aList = []
length = 80
for line in open("C:/Python27/trainning/test2.fa"):
    if line[0] == '>':
        name = line.split()[0]
        if aList:
            seq = ''.join(aList)    #将列表的元素合并成str
            for i in range(0,len(seq),length):
                #print i
                print seq[i:i+length]   #str的选取有区间
            aList=[]
        print name
    else:
        aList.append(line.strip())   #这里是列表，不是str

seq = ''.join(aList)
for i in range(0,len(seq),length):
    print seq[i:i+length]