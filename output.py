#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 29/5/2017 11:18 AM
 @Author  : Qiang,Q
 @File    : output.py
 @Software: PyCharm Community Edition
'''
import json
import csv
class Outputer(object):
    def __init__(self):
        self.datas=[]
    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    #json输出.
    def json_output(self):
        #'a' 以追加模式打开
        fout=open('/Users/fiona/Desktop/TestData/lianjiadata.json','a',encoding='utf-8')
        try:
            dataLines=[json.dumps(line,ensure_ascii=False)+'\n' for line in self.datas]
            fout.writelines(dataLines)
        finally:
            fout.close()

    #csv输出.
    def csv_output(self):
        csvFile=open('/Users/fiona/Desktop/TestData/lianjiadata.csv','a',encoding='utf-8')
        try:
            writer=csv.writer(csvFile)
            dataLines=[]
            for data in self.datas:
                lineTuple=(data['address'], data['flood'], data['following'], data['content'], data['unit_price'],
                           data['total_price'])
                dataLines.append(lineTuple)

            writer.writerows([data for data in dataLines])
        finally:
            csvFile.close()






