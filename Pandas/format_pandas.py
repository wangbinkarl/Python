#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose: 根据分组样本从突变检出表中提取对应的panel位点的突变信息，未提取出的从对应样本的tag.tsv中提取. 
# Author: Wangb
# Note:
# Last updated on: 20- -
import sys
import pandas as pd

panel_demo = pd.read_excel('/GPFS06/AnalysisTemp06/cln07/200528_project/panel_demo.xlsx',encoding="utf-8")

sample_ID_maching = pd.read_excel('/GPFS06/AnalysisTemp06/cln07/200528_project/sample_ID.xlsx',encoding="utf-8")
sample_ID_maching.columns = ['Cell line ID','Tumor proportion','Sample ID','Sid']

mutant_out = pd.read_excel('/GPFS06/AnalysisTemp06/cln07/200528_project/mutant_out.xlsx',encoding="utf-8")
new_mutant_out =  mutant_out.loc[:,[' Geneseeq sample ID','Gene','Type','AAChange','Chromosome','Chr.start','Chr.end']]
new_mutant_out.columns = ['sampleID','Gene','Type','AAChange','Chromosome','Chr.start','Chr.end']
new_mutant_out['Type'] = "Y|" + new_mutant_out['Type']

def single_group(panel_demo,sample_ID_maching,new_mutant_out,group):
		#按组别处理，最后合并所有组
		panel_demo_chr1 = panel_demo.loc[panel_demo['Cell line ID']==group,:]
		#取出组中所有样本
		testname_list = sample_ID_maching.loc[sample_ID_maching['Cell line ID']==group,:]['Sid'].astype('str').values.tolist()
		#建立空DF
		result = pd.DataFrame(columns = ['Cell line ID', 'Chr', 'Position', 'Ref', 'Alt', 'Gene', 'Tumor_AF', 'Variant Type'])

		for testname in testname_list:
				#提取ratio,例:0.002,0.0075
				ratio = sample_ID_maching.loc[sample_ID_maching['Sid']==testname,'Tumor proportion'].values[0]
				ratio = str(ratio)
				#从new_out中提取相关信息并格式化
				testname_df = new_mutant_out.loc[new_mutant_out['sampleID']==testname,:]
				testname_df['Ref'] = testname_df.AAChange.apply(lambda x: x.split(">")[0][-1])
				testname_df['Alt'] = testname_df.AAChange.apply(lambda x: x.split(">")[-1][0])
				testname_df['Chromosome'] = 'chr'+testname_df['Chromosome'].astype('str')
				testname_df.rename(columns={'Chr.start':'Position','Chromosome':'Chr'},inplace=True)
				#合并 panel_demo 与testname_df
				#add
				merge1 = pd.merge(panel_demo_chr1,testname_df,how='left',on = ['Chr','Position'])
				merge1.rename(columns={'Type':ratio,'Ref_x':'Ref','Alt_x':'Alt','Gene_x':'Gene'},inplace=True)
				merge1.drop(['sampleID','AAChange','Chr.end','Ref_y','Alt_y','Gene_y'], axis=1, inplace=True)

				#提取第二张表的信息
				tsv = pd.read_csv('/GPFS06/AnalysisTemp06/cln07/200528_project/Tag_tsv/{}.csv'.format(testname),sep=' ')
				tsv['Chr'] = tsv['Chr.start'].apply(lambda x: x.split(":")[0])
				tsv['Position'] = tsv['Chr.start'].apply(lambda x: x.split(":")[1])
				tsv['Position'] = tsv['Position'].astype('int')
				#add alt AF in TAGS
				tsv['TAGS'] = tsv['TAGS']+";AD:AF("+tsv['alt'].map(str)+";"+tsv['AF'].map(str)+")"	
				tsv['Chr'] = 'chr'+tsv['Chr']
				tsv['TAGS'] = 'N|'+tsv['TAGS']
				#tsv.rename(columns={'TAGS':ratio},inplace=True)
				#为了合并第表2的信息，需要进行将表1 的Na合并表2，在进行合并
				#拆分
				split_na = merge1.loc[merge1[ratio].isnull(),:]
				split_c1 = merge1.loc[~merge1[ratio].isnull(),:]
				#合并
				merge2 = pd.merge(split_na,tsv,how='left',on=['Chr','Position','Ref','Alt','Gene'])
				split_c2 =  merge2[['Cell line ID', 'Chr', 'Position', 'Ref', 'Alt', 'Gene', 'Tumor_AF', 'Variant Type','TAGS']]
				split_c2.rename(columns={'TAGS':ratio},inplace=True)
				#合并成总的表
				merge_suc = pd.concat([split_c1,split_c2],axis = 0)
				#追加
				result_tmp = pd.merge(merge_suc,result,how='left')
				result = result_tmp
		return result_tmp
#建立空DF
tmp_df = pd.DataFrame(columns = ['Cell line ID', 'Chr', 'Position', 'Ref', 'Alt', 'Gene', 'Tumor_AF', 'Variant Type','0.002','0.0075','0.015','0.05'])
for group in range(1,9):
	single_df = single_group(panel_demo,sample_ID_maching,new_mutant_out,group)
	merge_group = pd.concat([tmp_df,single_df],axis = 0)
	#设定列的顺序
	order_list = ['Cell line ID', 'Chr', 'Position', 'Ref', 'Alt', 'Gene', 'Tumor_AF', 'Variant Type','0.002','0.0075','0.015','0.05']
	merge_groupx = merge_group[order_list]
	tmp_df = merge_groupx
merge_groupx.to_excel('final.3.0.xlsx',header = True,index = False)
merge_groupx.to_csv('final.3.0.csv',header = True,index = False)
