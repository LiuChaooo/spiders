# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import scrapy
# from settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline
import redis
# import pymongo

from scrapy.exporters import CsvItemExporter

from datetime import datetime

# class UTCPipeline(object):
#     def process_item(self, item, spider):
#         #utcnow() 是获取UTC时间
#         item["crawled"] = str(datetime.utcnow())
#         # item["crawled"] = datetime.utcnow()
#         # 爬虫名
#         item["spider"] = spider.name
#         return item


class Tc58Pipeline(ImagesPipeline):

    def get_media_requests(self, item, info):  # 重写
        image_link = item['image_link']
        yield scrapy.Request(image_link)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        os.rename(images_store + image_path[0], images_store + item['detail_title'] + item["image_link"][-15:])

        return item


class Tc58JsonPipeline(object):
    def open_spider(self, spider):
        self.f = open('tc58.json','w')

    def process_item(self, item, spider):
        # item["spider"] = spider.name
        # json文件：unicode转encond("utf-8")
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()


class Tc58CSVPipeline(object):
    def open_spider(self, spider):
        # 创建csv文件对象，拥有写权限
        self.csv = open("gav.csv", "w")
        # 查创建一个Csv文件读写对象，参数是csv文件对象
        self.csvexporter = CsvItemExporter(self.csv)
        # 指定读写权限，可以开始写入数据
        self.csvexporter.start_exporting()

    def process_item(self, item, spider):
        # 将item数据写入到csv文件里
        self.csvexporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 表述数据写入结束
        self.csvexporter.finish_exporting()
        self.csv.close()


class Tc58RedisPipeline(object):
    def open_spider(self,spider):
        self.redis_cli = redis.Redis(host='127.0.0.1',port=6379)

    def process_item(self,item, spider):
        # 将item转换成json格式
        content = json.dumps(dict(item), ensure_ascii=False)
        # 将数据写入到list里，key GAV， value content
        self.redis_cli.lpush("GAV", content)
        return item


# class Tc58MongoPipeline(object):
#     def open_spider(self, spider):
#         # 创建MongoDb数据库链接对象
#         self.mongo_cli = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
#         # 创建MongoDB的数据库
#         self.dbname = self.mongo_cli["GAV"]
#         # 创建数据库的表
#         self.sheet = self.dbname["GAV_data"]
#
#     def process_item(self, item, spider):
#         # 将数据插入到表里
#         self.sheet.insert(dict(item))
#         return item



# class Tc58Pipeline(object):
#     def process_item(self, item, spider):
#         return item
