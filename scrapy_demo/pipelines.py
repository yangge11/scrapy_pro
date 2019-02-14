# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_demo.dao.dao_item import post_item


class ScrapyDemoPipeline(object):
    def process_item(self, item, spider):
        print 123456
        # post_item(item)
        # return item
