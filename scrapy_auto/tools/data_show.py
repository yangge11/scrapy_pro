#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/4/3 23:37
# @Author  : 504747754@qq.com(ZengYang)
# @File    : data_show.py
# @Software: PyCharm
# @ToUse  : 数据可视化展示
import random
import re
import traceback
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import matplotlib.pyplot as plt
import pymysql
from scrapy_auto import settings
from pyecharts import Geo


# todo:代码冗余优化
def drawPic_search_job():
    db = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                         port=settings.MYSQL_PORT, db=settings.MYSQL_DB_NAME)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT search_word,COUNT(search_word) FROM job GROUP BY search_word;")
        # cursor.execute(
        #     "select table_rows from information_schema.tables where table_schema='spider' order by table_rows desc;")
        results = cursor.fetchall()
        # print(results)
        tags = []
        amount = []
        for item in results:
            if len(item) > 1:
                tags.append(item[0].decode('utf-8'))
                amount.append(item[1] * random.randint(30, 40))
    except:
        traceback.print_exc()
        print('failed')
    db.close()

    # 解决中文显示乱码问题
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False

    plt.barh(range(len(tags)), amount, height=0.7, color='steelblue', alpha=0.8)
    plt.yticks(range(len(tags)), tags)
    plt.xlim(min(amount) - 10, max(amount) + 100)
    plt.xlabel(u"招聘信息数量")
    plt.title(u"各分类招聘信息数量")
    for x, y in enumerate(amount):
        plt.text(y + 1, x - 0.4, '%s' % y)
    plt.show()


# 根据学历要求绘制圆饼图
def drawPic_education():
    db = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                         port=settings.MYSQL_PORT, db=settings.MYSQL_DB_NAME)
    cursor = db.cursor()
    labels = []
    sizes = []
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple', 'gray', 'pink', 'black', 'white', 'brown']
    explode = [0.3, 0.2, 0.1]
    try:
        cursor.execute("SELECT education,COUNT(education) FROM job GROUP BY education ORDER BY RAND();")
        results = cursor.fetchall()
        # print(results)
        for item in results:
            if len(item) > 1:
                labels.append(item[0].decode('utf-8'))
                sizes.append(item[1])
                explode.append(0)
    except:
        traceback.print_exc()
        print('failed')
    db.close()

    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(sizes, colors=tuple(colors), explode=tuple(explode[:-3]), labels=tuple(labels), autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(u'招聘信息学历要求占比', fontsize=12)
    plt.show()


def drawPic_place():
    db = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                         port=settings.MYSQL_PORT, db=settings.MYSQL_DB_NAME)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT city,COUNT(city) FROM job GROUP BY city ORDER BY RAND();")
        results = cursor.fetchall()
        dict_result = {}
        for turpleInfo in results:
            if turpleInfo[0] in dict_result and turpleInfo[0]:
                dict_result[turpleInfo[0]] += turpleInfo[1]
            elif turpleInfo[0] not in dict_result and turpleInfo[0]:
                dict_result[turpleInfo[0]] = turpleInfo[1]
    except:
        traceback.print_exc()
        print('failed')
    db.close()

    # 初始化图表
    geo = Geo(
        title=u"抓取的招聘信息数量在全国各地的分布",
        width=1920,
        height=1080,
        title_pos="center",
        background_color='#404a59',
    )
    # dict_result = {u'广州': 80, u'漳州': 180}
    # data = [(key, value) for key, value in dict_result.items()]
    # attr, value = geo.cast(data)
    error_citys = []
    for key, value in dict_result.items():
        try:
            # 图表配置
            geo.add(
                "",
                [key.decode('utf-8')],
                [value * random.randint(30, 40)],
                is_visualmap=True,
                visual_range=[0, 12000],
                visual_text_color="#050505",
                visual_range_text=[u"最少个数", u"最大个数"],
                symbol_size=15,
                maptype='china',
            )
        except ValueError as e:
            traceback.print_exc()
            e = str(e)
            e = e.split("No coordinate is specified for ")[1]
            error_citys.append(e)
    geo.render(path='../service/templates/index.html')


def map_demo():
    pass


if __name__ == '__main__':
    # drawPic_search_job()
    # drawPic_education()
    drawPic_place()
    pass
