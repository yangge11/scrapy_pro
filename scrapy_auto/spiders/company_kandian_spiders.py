import json
import time
import traceback

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest


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
        yield {'url': response._url}


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
    allowed_domains = ['toutiao.com']

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
        'CONCURRENT_REQUESTS': 100,
        # 'DOWNLOAD_DELAY': 0.1,
        'ITEM_PIPELINES': {

        }
    }

    rules = (
        Rule(LinkExtractor(allow=('.*/a\d+/.*')), callback='detail_article', follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains), callback='splash_request', follow=True),
    )

    def start_requests(self):
        url = 'https://www.toutiao.com'
        yield SplashRequest(url, dont_process_response=True, args={'wait': 0.5}, meta={'real_url': url})

    def splash_request(self, request):
        """
        :param request: Request对象（是一个字典；怎么取值就不说了吧！！）
        :return: SplashRequest的请求
        """
        # dont_process_response=True 参数表示不更改响应对象类型（默认为：HTMLResponse；更改后为：SplashTextResponse）
        # args={'wait': 0.5} 表示传递等待参数0.5（Splash会渲染0.5s的时间）
        # meta 传递请求的当前请求的URL
        return SplashRequest(url=request.url, dont_process_response=True, args={'wait': 0.5},
                             meta={'real_url': request.url})

    # def _requests_to_follow(self, response):
    #     """重写的函数哈！这个函数是Rule的一个方法
    #     :param response: 这货是啥看名字都知道了吧（这货也是个字典，然后你懂的ｄ(･∀･*)♪ﾟ）
    #     :return: 追踪的Request
    #     """
    #     if not isinstance(response, HtmlResponse):
    #         return
    #     seen = set()
    #     # 将Response的URL更改为我们传递下来的URL
    #     # 需要注意哈！ 不能直接直接改！只能通过Response.replace这个魔术方法来改！（当然你改无所谓啦！反正会用报错来报复你 (`皿´) ）并且！！！
    #     # 敲黑板！！！！划重点！！！！！注意了！！！ 这货只能赋给一个新的对象（你说变量也行，怎么说都行！(*ﾟ∀ﾟ)=3）
    #     newresponse = response.replace(url=response.meta.get('real_url'))
    #     for n, rule in enumerate(self._rules):
    #         # 我要长一点不然有人看不见------------------------------------newresponse 看见没！别忘了改！！！
    #         links = [lnk for lnk in rule.link_extractor.extract_links(newresponse)
    #                  if lnk not in seen]
    #         if links and rule.process_links:
    #             links = rule.process_links(links)
    #         for link in links:
    #             seen.add(link)
    #             r = self._build_request(n, link)
    #             yield rule.process_request(r)
