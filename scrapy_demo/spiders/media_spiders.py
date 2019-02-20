#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import logging
import time
import traceback

from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider

from scrapy_demo.items import MediaItem


class CommonSpider(CrawlSpider):
    DRIVER_FIREFOX_HOME = '/Users/tv365/geckodriver'
    login_url = ''
    account = ''

    def init_common_parser(self, account):
        item = MediaItem()
        item['account'] = account
        return item

    def start_requests(self):
        url = self.login_url
        items = []
        accounts = self.account
        for index in range(len(accounts)):
            account = accounts[index]
            item = self.init_common_parser(account)
            items.append(item)

        for item in items:
            logging.info('spider account %s start' % item['account']['user_name'])
            yield Request(url, meta={'cookiejar': index, 'account': item['account'], 'item': item},
                          callback=self.after_login, dont_filter=True)

    def x_path(self, response, rule):
        try:
            result = response.xpath(rule).extract()
        except:
            traceback.print_exc()
            logging.error('rule xpath perhaps wrong %s' % rule)
        return result


class BaiJiaSpider(CommonSpider):
    name = 'bai_jia_spider'
    _platformId = None
    _dt = None
    _single_item = {}
    account = 'bai_jia_account'
    login_url = 'http://baijiahao.baidu.com/builder/app/login'

    custom_settings = {
        'DOWNLOAD_DELAY': '0.5',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/json, text/javascript, */*; q=0.01,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
    }

    def after_login(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        url = 'https://baijiahao.baidu.com/builderinner/api/content/app/userScore'
        yield FormRequest(
            url=url,
            method='POST',
            callback=self.parse_index_pages_radia,
            cookies=cookie,
            meta={'item': item, 'cookie': cookie},
            dont_filter=True
        )

    def parse_index_pages_radia(self, response):
        item = response.meta['item']
        logging.debug('into parse_index_pages_radia, accountid %s' % item['account']['accountId'])
        cookie = response.meta['cookie']
        url = 'https://baijiahao.baidu.com/builder/author/home/index?'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_count_all,
                      dont_filter=True)

    def parse_index_pages_count_all(self, response):
        item = response.meta['item']
        logging.debug('into parse_index_pages_count_all, accountid %s' % item['account']['accountId'])
        cookie = response.meta['cookie']
        url = 'https://baijiahao.baidu.com/builder/author/statistic/appStatistic'
        yield FormRequest(
            url=url,
            callback=self.parse_index_pages_all_articles,
            formdata={'type': 'news', 'is_yesterday': 'false', 'stat': '0'},
            meta={'item': item, 'cookie': cookie},
            cookies=cookie,
            dont_filter=True
        )

    def parse_index_pages_all_articles(self, response):
        item = response.meta['item']
        logging.debug('into parse_index_pages_all_articles, accountid %s' % item['account']['accountId'])
        cookie = response.meta['cookie']
        url = 'https://baijiahao.baidu.com/builder/author/statistic/getFansBasicInfo?start=1&end=7&fans_type=new%%2Csum&sort=asc&is_page=0&show_type=chart'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages)

    def parse_user_pages(self, response):
        item = response.meta['item']
        logging.debug('into parse_user_pages, accountid %s' % item['account']['accountId'])
        cookie = response.meta['cookie']
        url = 'https://baijiahao.baidu.com/builder/author/income/incomeBaseInfo?startDate=1&endDate=7&pageIndex=1&num=10&listType=0&is_export=0'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_income_pages,
                      dont_filter=True)
