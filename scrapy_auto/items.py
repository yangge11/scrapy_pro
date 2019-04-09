# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


"""
   [Article_Title] [nvarchar](100) NULL, -- 文章标题 提取自网页HTML代码 
   [Article_Descr] [nvarchar](200) NULL, -- 文章描述 提取自网页HTML代码 
   [Article_Keywords] [nvarchar](200) NULL, -- 文章关键词 提取自网页HTML代码 
   [Article_fromURL] [nvarchar](300) NULL, -- 文章原始URL，也就是采集自那个网页的URL 

   [Article_H1] [nvarchar](200) NULL, -- 网页包含的H1标签内的内容(如果有多个，取第一个) 
   [Article_Lenth] [int] NULL, -- 文章字数 

   [Article_Descr_ByApp] [nvarchar](300) NULL, -- 文章描述 (通过第三方算法或者插件，分析正文算出的文章摘要) 
   [Article_Keywords_ByApp] [nvarchar](300) NULL, -- 文章关键词 (通过第三方算法或者插件，例如分词，分析正文算出的标签) 
   [Article_Note_ByApp] [nvarchar](300) NULL, -- 文章短语 (通过第三方算法或者插件，分析正文算出的短语，可参考: http://daohang.bitool.cn/info/view/?id=166696) 

   [Creat_Date] [smalldatetime] NULL, -- 入库日期+时间 

   [Article_Content_original] [nvarchar](max) NULL, -- 文章正文(原始，未作处理的) 
   [Article_Content_Clear] [nvarchar](max) NULL, -- 文章正文 清洗处理后
"""


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    descr = scrapy.Field()
    keywords = scrapy.Field()
    fromURL = scrapy.Field()
    h1 = scrapy.Field()
    lenth = scrapy.Field()
    descr_by_app = scrapy.Field()
    keywords_by_app = scrapy.Field()
    note_by_app = scrapy.Field()
    creat_date = scrapy.Field()
    content_original = scrapy.Field()
    content_clear = scrapy.Field()


class JobItem(scrapy.Item):
    city = scrapy.Field()
    skill = scrapy.Field()
    welfare = scrapy.Field()
    salary = scrapy.Field()
    education = scrapy.Field()
    url = scrapy.Field()
    search_word = scrapy.Field()
    sub_job_type = scrapy.Field()
    job_type = scrapy.Field()


class MediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index_pages = scrapy.Field()
    user_pages = scrapy.Field()
    income_pages = scrapy.Field()
    content_pages = scrapy.Field()
    account = scrapy.Field()


class MediaAddItem(scrapy.Item):
    title = scrapy.Field()