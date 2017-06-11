#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 24/5/2017 10:16 PM
 @Author  : Qiang,Q
 @File    : esf_spider.py
 @Software: PyCharm Community Edition
'''

from urllib.request import urlopen
from bs4 import  BeautifulSoup as BS
from output import Outputer
import url_manager

def getPageUrl(base_url):
    html=urlopen(base_url)
    bsobg = BS(html.read(),"lxml")
    print(base_url)
    parseHtml(base_url)
    try:
        page_div=bsobg.find("div",class_='page-box house-lst-page-box')
        page_totalcount= eval(page_div['page-data'])['totalPage']

        for page in list(range(1,page_totalcount+1)):
            if page !=1:
                url=base_url+'pg%d' % page
                print(url)
                parseHtml(url)
            parseHtml(base_url)
    except AttributeError as  e:
        print(e)
    except Exception as  e:
        print(e)



def parseHtml(page_url):
    output=Outputer()
    try:
        html = urlopen(page_url)
        bsobg = BS(html.read(), "lxml")
        #print(len(bsobg.select(".sellListContent")))
        li_tag_arr=bsobg.select(".sellListContent")[0].select("li")
        for li_tag in li_tag_arr:
            info_clear_div=li_tag.find("div",class_="info clear")
            #hose_title_tag=info_clear_div.find("div",class_="title").select("a")[0]
            #print(hose_title_tag.get_text())
            # house_address_tag.get_text()
            ##house_address_tag.get_text()
            #建国门北大街  | 2室1厅 | 57.89平米 | 东南 西北 | 简装 | 有电梯
            house_address_tag = info_clear_div.find("div",class_="address")
            house_flood_tad=info_clear_div.find("div",class_="flood")
            house_following_info=info_clear_div.find("div",class_="followInfo")
            tag=info_clear_div.find("div",class_="tag").select('span')
            info_cont=''
            for info in tag:
                info_cont='%s | %s'%(info_cont,info.get_text())

            info_cont = info_cont.replace('|','',1)
            price_tag=info_clear_div.find('div',class_='priceInfo').select('div')
            unit_price=price_tag[1].get_text()
            total_price=price_tag[0].get_text()
            data={}
            data['address']=house_address_tag.get_text()
            data['flood']=house_flood_tad.get_text()
            data['following']=house_following_info.get_text()
            data['content']=info_cont
            data['unit_price']=unit_price
            data['total_price']=total_price
            output.collect_data(data)
    except:
        print('craw faild')
    finally:
        output.json_output('ershoufang')
        #output.csv_output()



def main():
    #
    # urls=url_manager.UrlManager()
    # base_url_list=urls.get_url('ershoufang')
    #
    # for url in base_url_list:
    #     getPageUrl(url)
    getPageUrl('https://bj.lianjia.com/ershoufang/pinggu/')

if __name__=='__main__':
    main()