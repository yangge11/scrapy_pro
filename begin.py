#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/3/19 23:39
# @Author  : 504747754@qq.com(ZengYang)
# @File    : begin.py
# @Software: PyCharm
# @ToUse  :


from scrapy import cmdline

# cmdline.execute("scrapy crawl boss_spider".split())
# cmdline.execute("scrapy crawl xici_spider -o proxy_list.json".split())
# cmdline.execute("scrapy crawl demo_spider".split())
# cmdline.execute("scrapy crawl toutiao_add_spider -o items.json".split())
# cmdline.execute("scrapy crawl toutiao_all_spider -o items.json".split())
# cmdline.execute("scrapy crawl lanzhou_spider -o items.json".split())
cmdline.execute("scrapy crawl bili_spider".split())






