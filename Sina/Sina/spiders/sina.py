# -*- coding: utf-8 -*-
import os
import scrapy
import time
from bs4 import BeautifulSoup
from Sina.items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        soup = BeautifulSoup(response.body, 'lxml')
        # 获取每个大块
        block_list = section = soup.find(id='tab01').find_all('div')[:-1]

        items = []
        # t1 = time.time()
        for block in block_list:
            # item = SinaItem() 不能在这儿创建,每一个小类中的每一条新闻对应一个对象

            # 获取大类的标题,在本地磁盘中创建大类的路径
            origin_title = block.find('h3').get_text()
            origin_link = block.find('a').get_text()
            ori_filename = './data/' + origin_title
            if not os.path.exists(ori_filename):
                origin_filename = os.makedirs(ori_filename)

            # 获取小类的标题,在对应的大类下创建小类的路径
            mid_title_list = block.find_all('li')
            for mid_title in mid_title_list:
                mtitle = mid_title.get_text()
                # print mtitle
                # print '*'*30
                mlink = mid_title.find('a').get('href')

                item = SinaItem()
                # 大类
                item['origin_title'] = origin_title
                item['origin_link'] = origin_link
                # 小类
                item['mid_title'] = mtitle
                item['mid_link'] = mlink

                m_filename = ori_filename + '/' + mtitle
                if not os.path.exists(m_filename):
                    mid_filename = os.makedirs(m_filename)

                items.append(item)
                # 发送每个小类的链接,并把大类小类的链接通过meta传送到response,回调函数使用
                yield scrapy.Request(url=mlink, meta={'meta1':item}, callback=self.parse_mid)

        # for item in items:
            # yield scrapy.Request(url=item['mid_link'], meta={'meta1':item,'time':t1}, callback=self.parse_mid)


    def parse_mid(self, response):
        meta_1 = response.meta['meta1']
        # t1 = response.meta['time']
        # t2 = time.time()
        # print '*'*50
        # print t2-t1