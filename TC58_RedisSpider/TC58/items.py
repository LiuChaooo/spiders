# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tc58Item(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 房源编号
    house_id = scrapy.Field()
    # 更新时间
    time = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 租赁方式
    rent_type = scrapy.Field()
    # 房屋类型
    house_class = scrapy.Field()
    # 朝向
    dest_floor = scrapy.Field()
    # 小区
    area = scrapy.Field()
    # 地址
    site = scrapy.Field()
    # 详细地址
    site_detail = scrapy.Field()
    # 联系电话
    contact_phone = scrapy.Field()
    # 联系人姓名
    contact_name = scrapy.Field()
    # 联系人公司
    contact_company = scrapy.Field()
    # 房源详情
    house_detail = scrapy.Field()
        # 设施:device
        # 描述:content
    # 小区详情
    area_detail = scrapy.Field()
        # 建筑年代：build_year
        # 建筑类型：build_class
        # 物业费用：property
        # 商圈：business
