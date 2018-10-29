# -*- coding: UTF-8 -*-
#文件之间的交并集

s1 = set(open("C:/Python27/trainning/file1").readlines())
s2 = set(open("C:/Python27/trainning/file2").readlines())

aList = list(s1.intersection(s2))
aList1 = list(s1.union(s2))
aList2 = list(s1.difference(s2).union(s2.difference(s1)))

print 'ins:',
for line in aList:
    lines = line.strip()
    print lines,
print ''
print 'uni:',
for line in aList1:
    lines = line.strip()
    print lines,
print ''
print 'dif:',
for line in aList2:
    lines = line.strip()
    print lines,