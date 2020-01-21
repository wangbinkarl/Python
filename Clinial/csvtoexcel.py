#!/usr/bin/env python
import os
import glob
import csv
from xlsxwriter.workbook import Workbook
import sys
csv.field_size_limit(sys.maxsize)
if len(sys.argv) < 2:
    print "py [csv tsv]"
    exit(1)

reload(sys)
sys.setdefaultencoding('utf8')

#for csvfile in glob.glob(os.path.join('.', '*.csv')):
samplename = sys.argv[1][:-4]

if sys.argv[1].endswith("csv"):
    workbook = Workbook(samplename + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()
if sys.argv[1].endswith("tsv"):
#for tsvfile in glob.glob(os.path.join('.', '*.tsv')):
    workbook = Workbook(samplename + '.xlsx', {'strings_to_urls': False})
    worksheet = workbook.add_worksheet()
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()
