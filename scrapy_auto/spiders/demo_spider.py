#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/23 18:44
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : demo_spider.py
# @Software: PyCharm
# @ToUse  :
import scrapy
from scrapy import Request

from scrapy_auto.items import JobItem


class Demo1(scrapy.Spider):
    """
    测试spider的各种操作
    """
    name = 'demo_spider'
    start_urls = [
        'https://www.baidu.com/'
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'DOWNLOAD_DELAY': 0.1,
    }

    def parse(self, response):
        yield Request(url='https://www.baidu.com/', callback=self.demo_item)

    def demo_item(self, response):
        while True:
            item = JobItem()
            for filed in item.fields.keys():
                item[filed] = 'demo'
            yield item
        pass
