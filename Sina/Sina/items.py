# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # 大类
    origin_title = scrapy.Field()
    origin_link = scrapy.Field()
    # 小类
    mid_title = scrapy.Field()
    mid_link = scrapy.Field()
    # 列表页
    news_title = scrapy.Field()
    news_link = scrapy.Field()
    # 详情页
    news_content = scrapy.Field()
