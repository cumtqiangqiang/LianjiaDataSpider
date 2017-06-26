# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# '''
#  @Time    : 12/6/2017 10:27 PM
#  @Author  : Qiang,Q
#  @File    : test.py
#  @Software: PyCharm Community Edition
# '''
#
# import socks
# import socket
# import time
# from stem.control import Controller
# from stem import Signal
# import requests
# from bs4 import BeautifulSoup
# err = 0
# counter = 0
# url = "checkip.dyn.com"
#
# if __name__ == '__main__':
#
#     with Controller.from_port(port = 9151) as controller:
#         try:
#             controller.authenticate()
#             socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
#             socket.socket = socks.socksocket
#             while counter < 10:
#                 r = requests.get("http://checkip.dyn.com")
#                 soup = BeautifulSoup(r.content)
#                 print(soup.find("body").text)
#                 counter = counter + 1
#                 #wait till next identity will be available
#                 controller.signal(Signal.NEWNYM)
#                 time.sleep(controller.get_newnym_wait())
#         except requests.HTTPError:
#             print("Could not reach URL")
#             err = err + 1
#     print("Used " + str(counter) + " IPs and got " + str(err) + " errors")
