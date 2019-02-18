#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/24 11:09
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : cnys_spider.py
# @Software: PyCharm
# @ToUse  :
import sys  # 引用sys模块进来，并不是进行sys的第一次加载
import traceback

from scrapy_demo.config import parser_config
from scrapy.linkextractors import LinkExtractor

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数
import time
from collections import Counter
import jieba
from scrapy.spiders import Rule, CrawlSpider
from scrapy_demo.items import ArticleItem

from scrapy_demo.parsers.common_parser import del_html_attr, get_CN_str


class SpiderAll(CrawlSpider):

    def parse_article(self, response):
        item = ArticleItem()
        for key in parser_config['all_spider'].keys():
            try:
                item[key] = response.xpath(parser_config['all_spider'][key]).extract()[0].encode('utf-8') if len(
                    response.xpath(parser_config['all_spider'][key]).extract()) > 0 else ''
            except:
                traceback.print_exc()
        for key in parser_config[self.name].keys():
            try:
                item[key] = response.xpath(parser_config[self.name][key]).extract()[0].encode('utf-8') if len(
                    response.xpath(parser_config[self.name][key]).extract()) > 0 else ''
            except:
                traceback.print_exc()
        # url无法分辨的时候使用
        if item['content_original'] == '':
            self.log('*** not article url for %s' % response._url.encode('utf-8'))
            return
        item['fromURL'] = response._url.encode('utf-8')
        item['creat_date'] = time.strftime("%Y/%m/%d %H:%M:%S")
        item['content_clear'] = del_html_attr(item['content_original']).encode('utf-8')
        item['lenth'] = len(item['content_clear'].replace(' ', ''))

        jieba.enable_parallel(20)
        cn_str = get_CN_str(item['content_clear'])
        words = [x.encode('utf-8') for x in jieba.cut_for_search(cn_str)]
        article_keywords = [x for x in words if len(x) >= len('标签')]
        article_descr = [x for x in words if len(x) >= len('分词短语')]
        article_note = [x for x in words if len(x) >= len('分词文章摘要')]
        jieba.disable_parallel()

        article_keywords = Counter(article_keywords).most_common(20)
        article_descr = Counter(article_descr).most_common(10)
        article_note = Counter(article_note).most_common(5)
        item['keywords_by_app'] = ','.join([c[0] for c in article_keywords])
        item['descr_by_app'] = ','.join([c[0] for c in article_descr])
        item['note_by_app'] = ','.join([c[0] for c in article_note])
        return item

    def parse_content_answer(self, response):
        # todo:
        item = ArticleItem()
        '哈哈asas<>'
        return item


class CNYSSpider(SpiderAll):
    name = 'cnys_spider'
    allowed_domains = ['cnys.com']
    start_urls = [
        'http://www.cnys.com/',
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'DEPTH_LIMIT': 0,
    }

    rules = (
        Rule(LinkExtractor(allow='article/\d+.html$'), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, attrs=('href', 'src')), follow=True),
    )


class W39Spider(SpiderAll):
    """
    http://tj.39.net/a/20111012/1822655.html
    http://ask.39.net/question/49726864.html
    """
    name = 'w39_spider'
    allowed_domains = ['39.net']
    start_urls = [
        'http://www.39.net/',
    ]
    rules = (
        Rule(LinkExtractor(allow='a/.*html$'), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow='question/.*html$'), callback='parse_content_answer', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains), follow=True),
    )


class VeryWellHealthSpider(SpiderAll):
    name = 'verywellhealth_spider'
    allowed_domains = ['verywellhealth.com']

    start_urls = [
        'https://www.verywellhealth.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*-\d+.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class HealthSpider(SpiderAll):
    name = 'health_spider'
    allowed_domains = ['health.com']

    start_urls = [
        'https://www.health.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class EditionHealthSpider(SpiderAll):
    name = 'edition_health_spider'
    allowed_domains = ['edition.cnn.com']

    start_urls = [
        'https://edition.cnn.com/health',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class WebmdSpider(SpiderAll):
    name = 'webmd_spider'
    allowed_domains = ['webmd.com']

    start_urls = [
        'https://www.webmd.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class WikihowSpider(SpiderAll):
    name = 'wikihow_spider'
    allowed_domains = ['wikihow.com']

    start_urls = [
        'https://www.wikihow.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class ToutiaoSpider(SpiderAll):
    name = 'toutiao_spider'
    allowed_domains = ['toutiao.com']

    start_urls = [
        'https://www.toutiao.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class HealthSohuSpider(SpiderAll):
    name = 'health_sohu_spider'
    allowed_domains = ['health.sohu.com']

    start_urls = [
        'http://health.sohu.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class HealthSinaSpider(SpiderAll):
    name = 'health_sina_spider'
    allowed_domains = ['health.sina.com']

    start_urls = [
        'http://health.sina.com.cn/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class AnswersSpider(SpiderAll):
    name = 'answers_spider'
    allowed_domains = ['answers.com']

    start_urls = [
        'http://www.answers.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class Ask39Spider(SpiderAll):
    name = 'ask_39_spider'
    allowed_domains = ['ask.39.net']

    start_urls = [
        'http://ask.39.net/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class AnswersYahooSpider(SpiderAll):
    name = 'answers_yahoo_spider'
    allowed_domains = ['answers.yahoo.com']

    start_urls = [
        'https://answers.yahoo.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class ZhidaoBaiduSpider(SpiderAll):
    name = 'zhidao_baidu_spider'
    allowed_domains = ['zhidao.baidu.com']

    start_urls = [
        'https://zhidao.baidu.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


class EditionSpider(SpiderAll):
    name = 'edition_health_spider'
    allowed_domains = ['edition.cnn.com/health']
    'https://edition.cnn.com/2019/02/13/health/nuedexta-doj-investigation-invs/index.html'

    start_urls = [
        'https://edition.cnn.com/health',
    ]
    rules = (
        Rule(LinkExtractor(allow=('.*')), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=('://.*/.*login.*',)), follow=True),
    )


'https://edition.cnn.com/health'


class DemoSpider(SpiderAll):
    name = 'wsj_spider'
    allowed_domains = ['wsj.com']

    start_urls = [
        'https://www.wsj.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow='articles/.*', attrs=('href',), ), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains), follow=True),
    )
