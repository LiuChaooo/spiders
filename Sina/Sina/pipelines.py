# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaPipeline(object):

    def process_item(self, item, spider):
        # if item['news_content'].strip():
        f = open(item['mid_filename'] + '/' + item['news_title'] + '.txt', 'w')
        f.write(item['news_content'].encode('utf-8'))
        f.close()

        return item