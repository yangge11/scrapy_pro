#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/24 21:02
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : dao_item.py
# @Software: PyCharm
# @ToUse  :


"""
CREATE TABLE [dbo].[Article_List]( 

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

   [Article_Type] [tinyint] NULL, -- 信息类型 0=新闻类(默认) 1=问答类 
   [Article_Content_Answer] [nvarchar](max) NULL, -- 问答类的回帖内容，多个回帖也放置于本字段，用分隔符分开。
   
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
"""

import pymssql
import traceback


def post_item(item):
    try:
        # todo:根据url作为唯一标准，进行update和新增操作
        server = "ip:port"
        user = "name"
        password = "pwd"
        database = "db_name"
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        sql = "INSERT INTO Article_List (Article_Title, Article_Descr, Article_Keywords,Article_fromURL,Article_H1,Article_Lenth,Article_Descr_ByApp," \
              "Article_Keywords_ByApp,Article_Note_ByApp,Creat_Date,Article_Content_original,Article_Content_Clear,Article_Type,Article_Content_Answer) " \
              "VALUES ('%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s' ,%s ,'%s')" % (
                  item['title'], item['descr'], item['keywords'], item['fromURL'], item['h1'], item['lenth'],
                  item['descr_by_app'], item['keywords_by_app'], item['note_by_app'], item['creat_date'],
                  item['content_original'], item['content_clear'], 0, '')
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        traceback.print_exc()
    pass


if __name__ == '__main__':
    post_item('')
