#coding=utf-8
import requests
import json
from threading import Thread
from lxml import etree
from Queue import Queue



class ChooseProxy(Thread):
    def __init__(self,p,g):
        # Thread.__init__(self)
        super(ChooseProxy, self).__init__()
        self.p = p
        self.g = g

    def run(self):
        url = 'http://www.baidu.com/'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449'}

        global SWITCH
        while SWITCH:
            try:
                proxy = self.p.get()
                response = requests.get(url, headers=headers, proxies=proxy, timeout=3)
                self.g.put(proxy)
            except Exception as e:
                # pass
                print e

        # self.write(new_proxies)
        # print new_proxies


# def get_proxies():
#     '''抓取代理IP'''
#     #	print 'start get_proxies'
#     # url = 'http://www.proxy360.cn/Region/America'
#     url = 'http://www.proxy360.cn/Region/China'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449'}
#     response = requests.get(url, headers=headers).content
#     #        print response
#
#     html = etree.HTML(response)
#     dlist = html.xpath('//div[@id="ctl00_ContentPlaceHolder1_upProjectList"]/div')[1:]
#
#     proxies = []
#     for each in dlist:
#         proxy = {}
#         sproxy = {}
#         if each.xpath('.//span'):
#             ip = each.xpath('.//span/text()')[0].strip()
#             port = each.xpath('.//span/text()')[1].strip()
#             proxy['http'] = ip + ':' + port
#             sproxy['https'] = ip + ':' + port
#
#             proxies.append(proxy)
#             proxies.append(sproxy)
#
#     return proxies

global SWITCH
SWITCH = True


def main():
    proxies = eval(raw_input('代理池:'))
    # print proxies
    pQueue = Queue()
    for proxy in proxies:
        pQueue.put(proxy)

    gQueue = Queue()
    threads = []
    for i in range(3):
        t = ChooseProxy(pQueue,gQueue)
        t.start()
        threads.append(t)

    while not pQueue.empty():
        pass

    global SWITCH
    SWITCH = False

    for item in threads:
        item.join()

    usable_proxies = []
    while not gQueue.empty():
        usable_proxy =  gQueue.get()
        usable_proxies.append(usable_proxy)

    print usable_proxies

    print '完成'

if __name__ == '__main__':
    main()
