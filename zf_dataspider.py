#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 8/6/2017 8:51 PM
 @Author  : Qiang,Q
 @File    : zf_dataspider.py
 @Software: PyCharm Community Edition
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from output import Outputer
import url_manager


def getPageUrl(base_url):
    html = urlopen(base_url)
    bsobg = BS(html.read(), "lxml")
    print(base_url)
    try:
        page_div = bsobg.find("div", class_='page-box house-lst-page-box')
        page_totalcount = eval(page_div['page-data'])['totalPage']

        for page in list(range(1, page_totalcount + 1)):
            if page != 1:
                url = base_url + 'pg%d' % page
                print(url)
                #parseHtml(url)
            #parseHtml(base_url)
    except:
        print('parse page count error or this page has only one!!')


def parseHtml(page_url):
    output = Outputer()
    try:
        html = urlopen(page_url)
        bsobg = BS(html.read(), "lxml")
        li_tag_arr = bsobg.select(".house-lst")[0].select("li")
        for li_tag in li_tag_arr:
            info_clear_div = li_tag.find("div", class_="info-panel")
            #房子具体信息 几居室 面积等
            house_detail_info = info_clear_div.find("div", class_="where")
            #房子的楼层信息 建于某年
            house_info = info_clear_div.find("div", class_="con")

            tag = info_clear_div.find("div", class_="view-label left").select('span')
            #print(tag)
            info_cont = ''

            for info in tag :
                print(info.contents)
                for tag in info.contents:
                    print(type(tag))

                    print(tag)
                #print(info.children)
                #info_cont = '%s | %s' % (info_cont, info.get_text())
            print('======')
            #info_cont = info_cont.replace('|', '', 1)
            #print(info_cont)
            #价格
            price_tag = info_clear_div.find('div', class_='price')
            #更新时间
            updated_tag=info_clear_div.find('div',class_='price-pre')
            #多少人看过房子
            col_look_tag=info_clear_div.find('div',class_='square')

            # data = {}
            # data['address'] = house_address_tag.get_text()
            # data['flood'] = house_flood_tad.get_text()
            # data['following'] = house_following_info.get_text()
            # data['content'] = info_cont
            # data['unit_price'] = unit_price
            # data['total_price'] = total_price
            # output.collect_data(data)
    except:
        print('craw faild')
    finally:
        output.json_output()
        # output.csv_output()


def main():
    # urls = url_manager.UrlManager()
    # base_url_list = urls.get_url('zufang')
    #
    # for url in base_url_list:
    #     getPageUrl(url)

    parseHtml('https://bj.lianjia.com/zufang/dongcheng/')

if __name__ == '__main__':
    print(type('a'))
    main()