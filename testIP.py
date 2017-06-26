#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 @Time    : 12/6/2017 9:42 PM
 @Author  : Qiang,Q
 @File    : testIP.py
 @Software: PyCharm Community Edition
'''
import socket
import socks
from urllib import request


def main():
    socks.set_default_proxy(socks.SOCKS5, 'localhost', 9050)
    socket.socket = socks.socksocket
    r = request.urlopen('http://icanhazip.com')

    print(r.read())


if __name__ == '__main__':
    main()


