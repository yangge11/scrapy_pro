import json
import logging
import time
import traceback

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest

script = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)
  splash:evaljs(js)
  assert(splash:wait(args.wait))
  return splash:html()
end
"""
demo = """
     yield SplashRequest(url, callback=self.parse, endpoint='execute',
                                    args={'lua_source': script, 'page': page, 'wait': 7})
"""


class TouTiaoSpider(CrawlSpider):
    custom_settings = {
        # 'HTTPERROR_ALLOWED_CODES': [301],
        'CONCURRENT_REQUESTS': 10,
        # 'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES': {

        }
    }

    def detail_article(self, response):
        # yield {'title': response.xpath("//title/text()").extract()[0]}
        # yield {'url': response._url}
        try:
            yield {'title': response.xpath("//title/text()").extract()[0], 'url': response._url}
        except:
            traceback.print_exc()
            logging.error('not match detail %s' % response._url)


class TouTiaoAddSpider(TouTiaoSpider):
    name = 'toutiao_add_spider'
    allowed_domains = ['toutiao.com']

    start_urls = [
        'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0',
    ]
    now_time_stamp = time.time()

    def parse(self, response):
        now_time_stamp_parse = time.time()
        urls_dict = json.loads(response.text)
        for url_dict in urls_dict['data']:
            yield Request(response.urljoin(url_dict['source_url']), callback=self.detail_article)
        next_max_behot_time = urls_dict['next']['max_behot_time']
        if now_time_stamp_parse - self.now_time_stamp <= 60 * 10:
            yield Request(
                'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=%s' % next_max_behot_time,
                callback=self.parse, priority=1)


class ToutiaoAllSpider(TouTiaoSpider):
    name = 'toutiao_all_spider'
    allowed_domains = ['www.toutiao.com']

    custom_settings = {
        # 渲染服务的url
        'SPLASH_URL': 'http://localhost:8050',

        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重过滤器
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 使用Splash的Http缓存
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'CONCURRENT_REQUESTS': 3,
        # 'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES': {

        },
        'LOG_LEVEL': 'INFO',
        # 'LOG_FILE': "/Users/xiaomayi/log/toutiao_all.log",
    }

    rules = (
        # todo:文章匹配规则优化
        Rule(LinkExtractor(allow_domains=allowed_domains, allow=('.*\d{1,}.*')),
             callback='detail_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains), process_request='splash_request', follow=True),
    )

    def start_requests(self):
        url = 'https://www.toutiao.com/a6676789786306413069/'
        yield SplashRequest(url, dont_process_response=True, args={'wait': 0.5},
                            meta={'real_url': url})

    def splash_request(self, request):
        return SplashRequest(url=request.url, dont_process_response=True, args={'wait': 0.5},
                             meta={'real_url': request.url})

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        try:
            newresponse = response.replace(url=response.meta.get('real_url'))
        except:
            traceback.print_exc()
            pass
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(newresponse)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            logging.info('%s response urls len %s' % (newresponse._url, len(links)))
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)


class ToutiaoAllSpider1(TouTiaoSpider):
    name = 'toutiao_all_spider1'

    custom_settings = {
        # 渲染服务的url
        'SPLASH_URL': 'http://localhost:8050',

        # 下载器中间件
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重过滤器
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # 使用Splash的Http缓存
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'CONCURRENT_REQUESTS': 3,
        # 'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES': {

        },
        'LOG_LEVEL': 'DEBUG',
        # 'LOG_FILE': "/Users/xiaomayi/log/toutiao_all.log",
    }

    def start_requests(self):
        url = 'https://search.jd.com/Search?keyword=%E8%A1%A3%E6%9C%8D'
        # url = 'https://www.toutiao.com/a6676789786306413069/'
        # url = 'http://gaia.imilive.cn/share.html?uid=0&videoid=116682377418697098&cc=TG45624'
        yield SplashRequest(url, dont_process_response=True, args={'wait': 15},
                            meta={'real_url': url}, callback=self.parse)

    def parse(self, response):

        pass

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        try:
            newresponse = response.replace(url=response.meta.get('real_url'))
        except:
            traceback.print_exc()
            pass
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(newresponse)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            logging.info('%s response urls len %s' % (newresponse._url, len(links)))
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)