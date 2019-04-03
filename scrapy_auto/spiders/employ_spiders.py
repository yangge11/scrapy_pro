#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/3/13 16:46
# @Author  : 504747754@qq.com(ZengYang)
# @File    : employ_spiders.py
# @Software: PyCharm
# @ToUse  : 抓取boss直聘岗位信息
import json
import logging
import traceback

import scrapy
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_auto.items import JobItem
from scrapy_auto.tools.convers import from_string_to_json


class BossZhiPin(CrawlSpider):
    name = 'boss_spider'
    allowed_domains = ['www.zhipin.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 3,
        'DOWNLOAD_DELAY': 1,
    }
    start_urls = [
        'https://www.zhipin.com/common/data/position.json',
    ]
    job_dict_mapping = {}  # 搜索词——岗位类别的映射

    # rules = (
    #     # Rule(LinkExtractor(allow='https://www.zhipin.com/c100010000/.query=.*&page=.*'), callback='parse_url',
    #     #      follow=True),
    #     Rule(LinkExtractor(allow='https://www.zhipin.com/job_detail/.*html$'), callback='parse_job', follow=True),
    #     Rule(LinkExtractor(allow_domains=allowed_domains), follow=True),
    # )

    def parse(self, response):
        """
        该函数仅抓取一次岗位目录数据
        """
        to_crawl_list = [
        ]
        dict_job = from_string_to_json(response.text)
        for job_type_dict in dict_job['data']:
            for sub_job_type_dict in job_type_dict['subLevelModelList']:
                for search_word_dict in sub_job_type_dict['subLevelModelList']:
                    to_crawl_list.append(search_word_dict['name'])
                    self.job_dict_mapping[search_word_dict['name']] = [job_type_dict['name'], sub_job_type_dict['name']]
        new_urls = ['https://www.zhipin.com/c100010000/?query=%s&page=1' % query_str for query_str in
                    set(to_crawl_list) if query_str in ['美工','记者','运营总监','活动策划']]
        # new_urls.append('https://www.zhipin.com/c100010000/?query=爬虫&page=1')
        for new_url in new_urls:
            item = JobItem()
            item['search_word'] = new_url.replace('https://www.zhipin.com/c100010000/?query=', '').replace('&page=1',
                                                                                                           '')
            item['job_type'] = self.job_dict_mapping[item['search_word']][0] if item['search_word'] in self.job_dict_mapping else ''
            item['sub_job_type'] = self.job_dict_mapping[item['search_word']][1] if item['search_word'] in self.job_dict_mapping else ''
            yield scrapy.Request(url=new_url, callback=self.parse_job_list, meta={'item': item})
            pass

    def parse_job_list(self, response):
        urls_detail = response.xpath('//ul/li//div[@class="info-primary"]//h3/a/@href').extract()
        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').extract()[0].encode('utf-8')
        for url_detail in urls_detail:
            yield scrapy.Request(url=response.urljoin(url_detail), callback=self.parse_job_detail,
                                 meta={'item': response.meta['item']})
        if next_page != 'javascript:;':
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_job_list,
                                 meta={'item': response.meta['item']})

    def parse_job_detail(self, response):
        """
        :param response:
        :return:
        """
        item = JobItem()
        item.update(response.meta['item'])
        item['city'] = response.xpath('//div[@class="info-primary"]/p/text()').extract()[0].encode('utf-8'). \
            replace('\t', '').replace('\n', '').replace(' ', '')
        item['skill'] = '###'.join(response.xpath('//div[@class="job-sec"]/div[@class="text"]/text()').extract()). \
            encode('utf-8').replace('\t', '').replace('\n', '').replace(' ', '')
        item['welfare'] = '###'.join(response.xpath('//div[@class="job-tags"]/span/text()').extract()). \
            encode('utf-8').replace('\t', '').replace('\n', '').replace(' ', '')
        item['salary'] = response.xpath('//div[@class="name"]/span[@class="salary"]/text()').extract()[0]. \
            encode('utf-8').replace('\t', '').replace('\n', '').replace(' ', '')
        item['education'] = response.xpath('//div[@class="info-primary"]/p/text()').extract()[2].encode('utf-8'). \
            replace('\t', '').replace('\n', '').replace(' ', '')
        item['url'] = response.url
        yield item