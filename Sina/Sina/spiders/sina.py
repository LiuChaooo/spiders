# -*- coding: utf-8 -*-
import os
import scrapy
from bs4 import BeautifulSoup
from Sina.items import *


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        soup = BeautifulSoup(response.body)
        # 获取每个大块
        block_list = section = soup.find(id='tab01').find_all('div')[:-1]
        for block in block_list:
            # item = SinaItem() 不能在这儿创建,每一个小类中的每一条新闻对应一个对象

            # 获取大类的标题,在本地磁盘中创建大类的路径
            origin_title = block.find('h3').get_text()
            origin_link = block.find('a').get_text()
            origin_filename = os.mkdir('./data/' + origin_title)

            # 获取小类的标题,在对应的大类下创建小类的路径
            mid_title_list = block.find_all('li')
            for mid_title in mid_title_list:
                mtitle = mid_title.get_text()
                mlink = mid_title.find('a').get('href')
                mid_filename = os.mkdir(origin_filename + '/' + mtitle)

                yield scrapy.Request(mlink, callback=self.parse_mid)

