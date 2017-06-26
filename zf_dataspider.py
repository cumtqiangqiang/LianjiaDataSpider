#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 8/6/2017 8:51 PM
 @Author  : Qiang,Q
 @File    : zf_dataspider.py
 @Software: PyCharm Community Edition
'''

from urllib import error
from bs4 import BeautifulSoup as BS
from bs4 import element
from output import Outputer
from  IP_Helper import  getProxy
import url_manager
import  random
import  time
from urllib.request import urlopen
from  urllib.request import  Request
from  urllib.request import ProxyHandler
from  urllib.request import build_opener
from  urllib.request import install_opener
import mysql.connector
import  sys
#reload(sys)


user_agent=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},\
    #本机的
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}]
IPSet = set()
IPlist=list()
def getPageUrl(base_url,IPs):


    req = Request(base_url, headers=random.choice(user_agent))
    print(random.choice(user_agent))
    html = urlopen(req, timeout=10)
    bsobg = BS(html.read(), "lxml")

    try:
        page_div = bsobg.find("div", class_='page-box house-lst-page-box')
        page_totalcount = eval(page_div['page-data'])['totalPage']

        for page in list(range(1, page_totalcount + 1)):
            if page != 1:
                url = base_url + 'pg%d' % page
                parseHtml(url,IPs)
            else:
                parseHtml(base_url,IPs)
    except AttributeError :
        print('parse page count error or this page has only one!!')


def parseHtml(page_url,IPs):
    output = Outputer()
    try:
        IP=random.choice(IPs)
        proxy = {'http': IP[0] + ':' + IP[1]}
        ip_helper=getProxy()
        if ip_helper.isAlive(IP[0],IP[1]):
            print(proxy)
            # 使用这个方式是全局方法。
            proxy_support = ProxyHandler(proxy)
            opener = build_opener(proxy_support)
            install_opener(opener)
            req=Request(page_url,headers=random.choice(user_agent))
            html = urlopen(req,timeout=10)
            bsobg = BS(html.read(), "lxml")
            house_list=bsobg.select(".house-lst")[0]
            nodata_tag=house_list.find('li',class_='list-no-data clear')
            if nodata_tag is None:
                li_tag_arr = house_list.select("li")
                for li_tag in li_tag_arr:
                    info_clear_div = li_tag.find("div", class_="info-panel")
                    #房子具体信息 几居室 面积等
                    house_info = info_clear_div.find("div", class_="where")
                    #房子的楼层信息 建于某年
                    flood_info = info_clear_div.find("div", class_="con")

                    tag = info_clear_div.find("div", class_="view-label left").select('span')
                    #地铁  供暖等
                    info_cont = ''
                    for info in tag :
                        #print(info.contents)
                        for info_detail in info.contents:
                            if(isinstance(info_detail,element.NavigableString)):

                                info_cont = '%s | %s' % (info_cont, info.get_text())

                    info_cont = info_cont.replace('|', '', 1)
                    #价格
                    price_tag = info_clear_div.find('div', class_='price')
                    #更新时间
                    updated_tag=info_clear_div.find('div',class_='price-pre')
                    #多少人看过房子
                    col_look_tag=info_clear_div.find('div',class_='square')

                    data = {}
                    data['house_info'] = house_info.get_text()
                    data['flood_info'] = flood_info.get_text()
                    data['following'] = col_look_tag.get_text()
                    data['content'] = info_cont
                    data['total_price'] = price_tag.get_text()
                    data['update_time']=updated_tag.get_text()
                    output.collect_data(data)
                output.json_output('zufang')
                print(page_url + ':craw success!!')
            else:
                print(page_url + ':this page is no data')
    except(error.HTTPError,error.URLError) as  e:
        print(e)
        output.error_log_output(url=page_url)
    except Exception as e:
        print(e)
        output.error_log_output(url=page_url)
    finally:
        time.sleep(1)


def getIPFromMysql():
    conn = mysql.connector.connect(user='root', password='123456', database="proxy")
    cursor = conn.cursor()
    query_cmd = '''
            select IP,PORT from proxy.PROXY;
            '''
    try:
        cursor.execute(query_cmd)
        values = cursor.fetchall()
        for row in values :
            IPSet.add(row)
        IPlist = list(IPSet)
        return IPlist
    except Exception as e:
        print(e)

def main():
    urls = url_manager.UrlManager()
    base_url_list = urls.get_url('zufang')
    IPs = getIPFromMysql()
    for url in base_url_list:
        getPageUrl(url,IPs)


if __name__ == '__main__':
     main()
