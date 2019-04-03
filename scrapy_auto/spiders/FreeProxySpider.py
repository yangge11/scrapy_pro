#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/4/1 20:40
# @Author  : 504747754@qq.com(ZengYang)
# @File    : FreeProxySpider.py
# @Software: PyCharm
# @ToUse  : 抓取免费代理站点的代理

"""
1.抓取代理
2.验证代理
3.存储备用
"""

import scrapy
from scrapy import Request
from scrapy.exporters import JsonItemExporter


class XiCiSpider(scrapy.Spider):
    name = 'xici_spider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [
        'https://www.xicidaili.com/nn'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
        },

    }

    def parse(self, response):
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            ip = sel.css('td:nth-child(2)::text').extract_first().encode('utf-8')
            port = sel.css('td:nth-child(3)::text').extract_first().encode('utf-8')
            scheme = sel.css('td:nth-child(6)::text').extract_first().lower().encode('utf-8')
            proxy = '%s://%s:%s' % (scheme, ip, port)
            meta = {
                'proxy': proxy, 'dont_retry': True, 'download_timeout': 10, '_proxy_scheme': scheme, '_proxy_ip': ip,
            }
            yield Request(url='%s://httpbin.org/ip' % scheme, callback=self.check_available, dont_filter=True,
                          meta=meta)

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        if proxy_ip in response.text:
            yield {'proxy_scheme': response.meta['_proxy_scheme'], 'proxy': response.meta['proxy'], }
