import json

import scrapy
from scrapy import Request, FormRequest


class LanZhouSpider(scrapy.Spider):
    name = "lanzhou_spider"
    custom_settings = {
        'COOKIES_ENABLED': False,
        'REDIRECT_ENABLED': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES': {
        },
        'ITEM_PIPELINES': {
        },
    }
    headers = {
        'accept': 'application/json, text/javascript, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded",
        "origin": "https://www.lanzous.com",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        'lx': 2,
        'fid': 978840,
        'uid': 243078,
        'pg': 1,
        'rep': 0,
        't': 1573626257,
        'k': 'de7b03b69ce05b9257d15ea31a00a6c2',
        'up': 1,
    }

    def start_requests(self):
        url = 'https://www.lanzous.com/b{item_id}'
        for item_id in range(12583, 20000):
            yield Request(url=url.format(item_id=item_id), headers=self.headers, meta={'fid': item_id})

    def parse(self, response):
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
        url = 'https://www.lanzous.com/filemoreajax.php'
        yield FormRequest(url, method='POST', headers=self.headers,
                          body='lx=2&fid={fid}&uid={uid}&pg=1&rep=0&t={t}&k={k}&up=1'.format(fid=self.data['fid'],
                                                                                             uid=self.data['uid'],
                                                                                             t=self.data['t'],
                                                                                             k=self.data['k'], ),
                          callback=self.parse_content, dont_filter=True, meta={'url': response.url})

    def parse_content(self, response):
        try:
            print('in parse_content')
            url = response.meta['url']
            content_json = json.loads(response.text)
            content = ''
            for name in content_json['text']:
                content += name['name_all']
            yield {'url': url, 'name': content}
        except:
            print('error')
