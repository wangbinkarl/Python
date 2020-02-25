#批量对标签进行t检验
from scipy import stats
import numpy as np
import pandas as pd
import math
#np.random.seed(12345678)
#rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
#rvs2 = stats.norm.rvs(loc=5,scale=10,size=500)
#res = stats.ttest_ind(rvs1,rvs2)
allinput = pd.read_csv("final_res.filter.csv",sep = ',',header=None)
#创建结果文件，292x292的矩阵
res_df = pd.read_csv("null_df.csv",sep = ',')
res_df = res_df.set_index("Unnamed: 0")
num = (allinput.shape[1])/2 + 1
for i in range(1,num):
        for j in range(i+1,num):
                allinputx = allinput.iloc[:,[i*2-1,i*2,j*2-1,j*2]]
                #标签A对标签B
                flag1_Y = allinputx[(allinputx[i*2-1]=='N') & (allinputx[j*2-1]=='Y')]
                flag1_N = allinputx[(allinputx[i*2-1]=='N') & (allinputx[j*2-1]=='N')]
                res = stats.ttest_ind(flag1_Y.iloc[:,3],flag1_N.iloc[:,3])
                res_df.iloc[j-1,i-1] = res[1]
                #标签B对标签A
                flag2_Y = allinputx[(allinputx[j*2-1]=='N') & (allinputx[i*2-1]=='Y')]
                flag2_N = allinputx[(allinputx[j*2-1]=='N') & (allinputx[i*2-1]=='N')]
                res2 = stats.ttest_ind(flag2_Y.iloc[:,3],flag2_N.iloc[:,3])
                res_df.iloc[i-1,j-1] = res2[1]

res_df.to_csv("t.test.csv",sep = ',')
