# scrapy_pro

scrapy备份记录：
1.debug启动：http://www.scrapyd.cn/jiaocheng/135.html
Run-》Edit Configurations……
2.scrapy相关设置
深度抓取有自己的设计逻辑；代理配置有自己的设计逻辑；redis分布式有自己的设计逻辑；

以下内容的应用：
name = "snys_spider"
    allowed_domains = ['cnys.com']
    start_urls = [
        'http://www.cnys.com/',
    ]
    rules = (
        Rule(LinkExtractor(allow=r"article/\d+.html$"), callback="parse_article", follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains)),
        # Rule(LinkExtractor(deny=r"/subject/\d+/reviews\?sort=time$")),
        # Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time\&start=\d+$")),
        # Rule(LinkExtractor(allow=r"/review/\d+/$"), callback="parse_review", follow=True),
    )    

#### Version
1.0
基本架构搭建，jieba分词处理，数据标签属性清洗 
#TODO:针对现有架构进行20个站点的试行开发，jieba算法的设计完善

