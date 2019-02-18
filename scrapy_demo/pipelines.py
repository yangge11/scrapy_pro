# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from twisted.enterprise import adbapi

from scrapy_demo.dao.dao_item import post_item


class ScrapyDemoPipeline(object):
    def process_item(self, item, spider):
        print 123456
        # post_item(item)
        # return item


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item


class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 从项目的配置文件中读取相应的参数
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'scrapy_default')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", 'root')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", 'new.1234')
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER,
                                            passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)
