# -*- coding: UTF-8 -*-
#将表达数据转换为矩阵形式
rList = []
tissueSet = set()
aDict = {}
for line in open("C:/Python27/trainning/multipleColExpr"):
    if line[0] == 'G':
        id = line.split()[0]
        #print id
    else:
        rowN = line.split()[0]
        colN = line.split()[1]
        expr = line.split()[2]
        if rowN not in aDict:
            aDict[rowN] = {}
        assert colN not in aDict[rowN],"Duplicate tissues"
        aDict[rowN][colN] = expr
        tissueSet.add(colN)

cList = list(tissueSet)
cList.sort()
print "%s\t%s" % (id,'\t'.join(cList))

for rowN,colN in aDict.items():
    #print "%s\t%s" % (rowN,colN)
    rowN1 = [rowN]
    for line in cList:
        rowN1.append(colN[line])
    print '\t'.join(rowN1)


'''
输出格式
Gene    A-431    A-549    AN3-CA    BEWO    CACO-2
ENSG00000000460    25.2    14.2    10.6    24.4    14.2
ENSG00000000938    0.0    0.0    0.0    0.0    0.0
ENSG00000000457    2.8    3.4    3.8    5.8    2.9
ENSG00000000419    73.8    38.6    33.9    53.7    155.5
ENSG00000000003    21.3    32.5    38.2    31.4    63.9
ENSG00000000005    0.0    0.0    0.0    0.0    0.0
'''