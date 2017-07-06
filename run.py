#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 5/7/2017 8:34 PM
 @Author  : Qiang,Q
 @File    : run.py
 @Software: PyCharm Community Edition
'''

import sys
from multiprocessing import Process

sys.path.append('../')

from IP_Helper import run as IPRefreshRun
from zf_dataspider import  run as  ZuFangDataRun


def run():
    p_list = list()
    p1 = Process(target=IPRefreshRun, name='IPRefreshRun')
    p_list.append(p1)
    p2 = Process(target=ZuFangDataRun, name='ZuFangDataRun')
    p_list.append(p2)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()

if __name__ == '__main__':
    run()
