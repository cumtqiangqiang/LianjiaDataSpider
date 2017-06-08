#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 29/5/2017 11:17 AM
 @Author  : Qiang,Q
 @File    : url_manager.py
 @Software: PyCharm Community Edition
'''
import itertools
#二手房的url
ERSHOU_URL_TEMPLATE = 'https://bj.lianjia.com/%s/%s/'
#新房的url
XIN_URL_TEMPLATE = 'https://bj.fang.lianjia.com/%s/%s/'
#租房的url
ZU_URL_TEMPLATE = 'https://bj.lianjia.com/%s/%s/'
REGION = (
'dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping', 'daxing',
'yizhuangkaifaqu', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun', 'yanqing')
TRADE_TYPE = ('ershoufang', 'loupan', 'zufang')
class UrlManager(object):
    def __init__(self):
        self.ershoufang_urls=list()
        self.xinfang_urls=list()
        self.zufang_urls=list()
        self.dict=dict()
        self.generateBaseUrl()


    def generateBaseUrl(self):
        template_urls=(ERSHOU_URL_TEMPLATE,XIN_URL_TEMPLATE,ZU_URL_TEMPLATE)
        lists=(self.ershoufang_urls,self.xinfang_urls,self.zufang_urls)
        for index in range(3):
            for region in REGION:
                url = template_urls[index] % (TRADE_TYPE[index], region)
                list=lists[index]
                list.append(url)
            self.dict[TRADE_TYPE[index]]=list


    def get_url(self,type):

        return self.dict[type]
