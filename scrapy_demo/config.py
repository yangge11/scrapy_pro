#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/28 15:04
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : config.py
# @Software: PyCharm
# @ToUse  :


parser_config = {
    'all_spider': {
        'title': '//title/text()',
        'descr': '//meta[@name="description"]/text()|//meta[@name="Description"]/text()',
        'keywords': '//meta[@name="keywords"]/text()|//meta[@name="Keywords"]/text()',
    },
    'cnys_spider': {
        'content_original': '//div[@class="reads"]',
    },
    'w39_spider': {
        'content_original': '//div[@class="art_con"]',
    },
    'verywellhealth_spider': {
        'content_original': '//div[@class="loc chop-content "]|//div[@class="comp right-rail__offset taxonomy article-content expert-content"]',
        # 'loc content l-main'，//article
    },
    'health_spider': {
        'content_original': '//div[@class="article-content-container two-col-content-container"]',
    },
    'wsj_spider': {
        'content_original': '//div[@class="wsj-snippet-body"]',
    },
}
