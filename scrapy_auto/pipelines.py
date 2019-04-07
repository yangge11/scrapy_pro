# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import logging
import time
import traceback

import pymongo
from scrapy.exporters import JsonItemExporter
from scrapy.utils.python import to_bytes
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.enterprise import adbapi


class ScrapyDemoPipeline(object):
    def process_item(self, item, spider):
        print(123456)
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
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'scrapy_default')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", '')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", '')
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER,
                                            passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8mb4')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def update_db(self, tx, item):
        values = (
            item['url'],
            item['city'],
            item['skill'],
            item['welfare'],
            item['salary'],
            item['education'],
            item['search_word'],
            item['sub_job_type'],
            item['job_type'],
            time.strftime("%Y/%m/%d %H:%M:%S"),
            time.strftime("%Y/%m/%d %H:%M:%S"),
        )
        sql = 'update job (`url`,`city`,`skill`,`welfare`,`salary`,`education`,`search_word`,`sub_job_type`,`job_type`,`create_time`,`update_time`) VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)
        pass

    def insert_db(self, tx, item):
        values = (
            item['url'],
            item['city'],
            item['skill'],
            item['welfare'],
            item['salary'],
            item['education'],
            item['search_word'],
            item['sub_job_type'],
            item['job_type'],
            time.strftime("%Y/%m/%d %H:%M:%S"),
            time.strftime("%Y/%m/%d %H:%M:%S"),
        )
        sql = 'INSERT INTO job (`url`,`city`,`skill`,`welfare`,`salary`,`education`,`search_word`,`sub_job_type`,`job_type`,`create_time`,`update_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            tx.execute(sql, values)
        except:
            # todo:数据库断开连接
            logging.error('error for mysql %s' % item['url'])
            traceback.print_exc()
            self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER,
                                                passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8mb4')
        pass

