import json

import scrapy
from scrapy import Request, FormRequest

from scrapy_auto.items import LanzouItem

"""
spiders目录:
用来写所有的爬虫spider
"""


class LanZhouSpider(scrapy.Spider):
    name = "lanzhou_spider"  # 唯一区分每个spider的方式
    custom_settings = {  # 每一个爬虫的自定义配置，settins.py是全局配置
        'COOKIES_ENABLED': False,
        'REDIRECT_ENABLED': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES': {  # 下载中间件，这里面配置你写好的下载中间件，数值越小，优先级越高
            # 'scrapy_auto.middlewares.RandomHttpProxyMiddleware': 543,  # 代理中间价
            # 'scrapy_auto.middlewares.RandomUAMiddleware': 501,  # 代理中间价
        },
        'SPIDER_MIDDLEWARES': {  # 爬虫中间件，这里面配置你写好的爬虫中间件，数值越小，优先级越高
        },
        'ITEM_PIPELINES': {  # 管道，控制你输出数据的方式，数值越小，优先级越高
            # 'scrapy_auto.pipelines.MySQLDemoPipeline': 1,
            'scrapy_auto.pipelines.ExcelPipeline': 10,
        },
    }
    headers = {  # 请求头
        'accept': 'application/json, text/javascript, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded",
        "origin": "https://www.lanzous.com",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {  # 请求的post数据
        'lx': 2,
        'fid': 978840,
        'uid': 243078,
        'pg': 1,
        'rep': 0,
        't': 1573626257,
        'k': 'de7b03b69ce05b9257d15ea31a00a6c2',
        'up': 1,
    }

    # start_urls = ['www.baidu.com', ]  # 爬虫会先从这些url进行采集

    def start_requests(self):  # 当看到这个函数的时候，就走这个函数，原先start_urls的url不再请求，爬虫第一次启动就进入的函数
        url = 'https://www.lanzous.com/b{item_id}'
        for item_id in range(12583, 12683):
            yield Request(url=url.format(item_id=item_id), headers=self.headers,
                          meta={'fid': item_id})  # meta是用来做数据间的传递的，Request是get请求构建的方式

    def parse(self, response): # 默认处理start_requests的请求，或者来自start_urls构建的请求
        # 一系列拼接和破解方式
        # 解析流程图：从start_requests==》parse，走了1，2，3，4，5，6，7这7个步骤
        self.data['fid'] = response.meta['fid']
        begin1_t = response.text.find("'t':") + len("'t':")
        end1_t = response.text.find(",", begin1_t)
        t_str = response.text[begin1_t:end1_t]
        begin1 = response.text.find("var %s = '" % t_str) + len("var %s = '" % t_str)
        end1 = response.text.find("'", begin1)
        self.data['t'] = response.text[begin1:end1]

        begin1_k = response.text.find("'k':") + len("'k':")
        end1_k = response.text.find(",", begin1_k)
        k_str = response.text[begin1_k:end1_k]
        begin = response.text.find("var %s = '" % k_str) + len("var %s = '" % k_str)
        end = response.text.find("'", begin)
        self.data['k'] = response.text[begin:end]

        begin_uid = response.text.find("'uid':'") + len("'uid':'")
        end_uid = response.text.find("'", begin_uid)
        self.data['uid'] = response.text[begin_uid:end_uid]
        print(self.data['t'], self.data['k'], self.data['uid'])

        # 下一个请求，FormRequest是post请求的构建方式，针对post请求，要加上dont_filter=True，callback这个请求交给哪个函数来处理
        url = 'https://www.lanzous.com/filemoreajax.php'
        yield FormRequest(url, method='POST', headers=self.headers,
                          body='lx=2&fid={fid}&uid={uid}&pg=1&rep=0&t={t}&k={k}&up=1'.format(fid=self.data['fid'],
                                                                                             uid=self.data['uid'],
                                                                                             t=self.data['t'],
                                                                                             k=self.data['k'], ),
                          callback=self.parse_content, dont_filter=True, meta={'url': response.url})

    def parse_content(self, response):
        try:
            item = LanzouItem()
            print('in parse_content')
            url = response.meta['url']
            content_json = json.loads(response.text)
            content = ''
            for name in content_json['text']:
                content += name['name_all']
            item['url'] = url
            item['name'] = content
            yield item # 一碰到yield item的时候，我们就开始走管道，存储数据
        except:
            print('error')
