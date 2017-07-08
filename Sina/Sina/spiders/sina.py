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
                item['mid_filename'] = m_filename
                if not os.path.exists(m_filename):
                    mid_filename = os.makedirs(m_filename)

                items.append(item)
                # 发送每个小类的链接,并把大类小类的链接通过meta传送到response,回调函数使用
                # yield scrapy.Request(url=mlink, meta={'meta1':item}, callback=self.parse_mid)

        for item in items:
            yield scrapy.Request(url=item['mid_link'], meta={'meta1':item}, callback=self.parse_mid)


    def parse_mid(self, response):
        meta_1 = response.meta['meta1']
        # t1 = response.meta['time']
        # t2 = time.time()
        # print '*'*50
        # print t2-t1
        # 抓取列表也的url
        list_urls =  response.xpath('//ul/li//a/@href').extract()
        list_title = response.xpath('//ul/li//a/text()').extract()
        # print len(url_list)
        items = []
        for url in list_urls:
            # print meta_1['mid_filename']
            # print '*'*50
            item = SinaItem()
            # 大类
            item['origin_title'] = meta_1['origin_title']
            item['origin_link'] = meta_1['origin_link']
            # 小类
            item['mid_title'] = meta_1['mid_title']
            item['mid_link'] = meta_1['mid_link']
            item['mid_filename'] = meta_1['mid_filename']
            # 列表页
            # item['news_link'] = url if url.startswith(item['origin_link']) else item['origin_link']+url
            item['news_link'] = url
            item['lnews_title'] = list_title

            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['news_link'], meta={'meta2':item}, callback=self.parse_detail)


    def parse_detail(self,response):
        import re
        meta2 = response.meta['meta2']


        contents_list = response.xpath('//p/text()').extract()
        contents = ''
        title = response.url[7:-6] if len(response.url[7:-6])>10 else meta2['lnews_title']
        # pattern = re.compile(r'.+?.cn/(.+/)')
        # if len(response.url[20:-6]) > 5:
        #     title = str(pattern.match(response.url).groups(1))
        # else:
        #     meta2['lnews_title']
        # print title
        title = title.replace('/','-')
        # print title.encode('utf-8') + '*'*30
        # print len(contents)
        for content in contents_list:
            if content.strip():
                contents += content.strip() + '\n'

                item = SinaItem()
                # 大类
                item['origin_title'] = meta2['origin_title']
                item['origin_link'] = meta2['origin_link']
                # 小类
                item['mid_title'] = meta2['mid_title']
                item['mid_link'] = meta2['mid_link']
                item['mid_filename'] = meta2['mid_filename']
                # 列表页
                item['news_link'] = meta2['news_link']
                # 详情页
                item['news_content'] = contents
                item['news_title'] = title

                yield item