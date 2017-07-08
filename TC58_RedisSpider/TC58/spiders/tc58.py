# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from TC58.items import *
from scrapy_redis.spiders import RedisSpider


class Tc58Spider(RedisSpider):
    name = 'tc58'
    allowed_domains = ['58.com']
    # start_urls = ['http://bj.58.com/chuzu/']
    redis_key = 'tc58:start_urls'



    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # print soup
        link_list = soup.find_all(class_='des')
        # print '获取的列表1长度是%d'%len(link_list)
        for link in link_list:
            new_url = link.find('a').get('href').strip()
            yield scrapy.Request(new_url, callback=self.parse_detail)

        pager_list = soup.find(class_='pager').find_all('a')
        # print '获取的列表2的长度是%d'%len(pager_list)
        for pager in pager_list:
            pager_url = pager.get('href').strip()
            yield scrapy.Request(pager_url, callback=self.parse)

    def parse_detail(self, response):
        item = Tc58Item()
        soup = BeautifulSoup(response.text, 'lxml')
        part1 = soup.find(class_='house-title')
        # 标题
        item['title'] = part1.find('h1').get_text().strip() if part1.find('h1') and part1 else 'NULL'
        if len(part1.find('p').get_text().strip().split('\n')) > 1:
            # 房源编号
            item['house_id'] = part1.find('p').get_text().strip().split('\n')[0].strip()
            # 更新时间
            item['time'] = part1.find('p').get_text().strip().split('\n')[1].strip()
        else:
            item['house_id'] = 'NULL'
            item['time'] = part1.find('p').get_text().strip().split('\n')[0].strip()
        # 价格
        item['price'] = soup.find(class_='c_ff552e').get_text()

        li_list = soup.find(class_='f14').find_all('li')
        # 租赁方式
        item['rent_type'] = li_list[0].find_all('span')[-1].get_text().strip() if li_list[0].find_all('span')[-1] else 'NULL'
        # 房屋类型
        item['house_class'] =','.join(li_list[1].find_all('span')[-1].get_text().split()) if li_list[0].find_all('span')[-1] else 'NULL'
        # 朝向楼层
        item['dest_floor'] = li_list[2].find_all('span')[-1].get_text().strip() if li_list[0].find_all('span')[-1] else 'NULL'
        # 小区
        item['area'] = li_list[3].find_all('span')[-1].get_text().strip() if li_list[0].find_all('span')[-1] else 'NULL'
        # 地址
        item['site'] = li_list[4].find_all('span')[-1].get_text().split()[0].strip() + li_list[4].find_all('span')[-1].get_text().split()[-1].strip() if li_list[0].find_all('span')[-1] else 'NULL'
        # 详细地址
        item['site_detail'] = li_list[5].find_all('span')[1].get_text().strip() if li_list[0].find_all('span')[1] else 'NULL'
        # 联系电话
        item['contact_phone'] = soup.find(class_='phone-num').get_text().strip() if soup.find(class_='phone-num') else 'NULL'
        # 联系人姓名
        item['contact_name'] = soup.find(class_='agent-name').get_text().strip() if soup.find(class_='agent-name') else 'NULL'
        # 联系人公司
        item['contact_company'] = soup.find(class_='agent-subgroup').contents[0].strip() if soup.find(class_='agent-subgroup') else 'NULL'
        # 房源详情
        # {'house_detail': {'device': [],'content': ''}
        house = {}
        # 设施:
        house['device'] = soup.find(class_='house-disposal').get_text().strip().split('\n') if soup.find(class_='house-disposal') else 'NULL'
        # 描述:
        house['content'] = soup.find(class_='a2').get_text() if soup.find(class_='a2') else 'NULL'
        item['house_detail'] = house
        # 小区详情
        if soup.find(class_='district-info-list'):
            build_list = soup.find(class_='district-info-list').find_all('li')
            building = {}
            building['build_year'] = build_list[0].find_all('span')[1].get_text().strip()
            building['build_class'] = build_list[1].find_all('span')[1].get_text().strip()
            building['property'] = build_list[-2].find_all('span')[1].get_text().strip()
            building['business'] = build_list[-1].find_all('span')[1].get_text().strip()
            item['area_detail'] = building
        else:
            item['area_detail'] = 'NULL'

        yield item