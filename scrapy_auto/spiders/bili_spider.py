# @Time : 2019/12/19 8:51 PM
# @Author : 504747754@qq.com(ZengYang)
# @File : bili_spider.py
# @Software : PyCharm
# @ToUse  :
import json
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider

# 1.了解爬虫执行原理 2.了解爬虫脚本 3.了解爬虫的框架 4.了解各种反爬
from scrapy_auto.items import BiliItem


class BiliSpider(CrawlSpider):
    """
    需求：采集b站番剧索引的151页的数据
    """
    name = 'bili_spider'
    url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize=20&type=1'
    custom_settings = {  # 每一个爬虫的自定义配置，settins.py是全局配置
        'ITEM_PIPELINES': {  # 管道，控制你输出数据的方式，数值越小，优先级越高
            'scrapy_auto.pipelines.ExcelBiliPipeline': 10,
        },
    }

    def start_requests(self):
        for pg in range(1, 2):
            yield Request(url=self.url.format(page=pg))

    def parse(self, response):
        item_list = json.loads(response.text)['data']['list']
        for item1 in item_list:
            item = BiliItem()
            item['is_vip'] = 1 if item1['badge'] else 0
            item['thumb'] = item1['cover']
            item['episode'] = re.findall('\d+', item1['index_show'])[0]
            item['is_finish'] = item1['is_finish']
            item['link_detail'] = item1['link']
            item['fans_info'] = item1['order']
            item['title'] = item1['title']
            yield item
        pass
