#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/3/19 23:39
# @Author  : 504747754@qq.com(ZengYang)
# @File    : begin.py
# @Software: PyCharm
# @ToUse  :


from scrapy import cmdline

cmdline.execute("scrapy crawl boss_spider".split())
