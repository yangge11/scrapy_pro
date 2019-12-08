#!/usr/bin/python
# @Time    : 2019/12/1 18:58
# @Author  : 504747754@qq.com(ZengYang)
# @File    : demo.py
# @Software: PyCharm
# @ToUse  :
import json
import re
import urllib
import ssl

import requests

ssl._create_default_https_context = ssl._create_unverified_context

def json_demo():
    dict1 = {"url": "https://www.lanzous.com/b12583", "name": "精品广场舞83-2.zip精品广场舞83-1.zip"}
    str1 = json.dumps(dict1)
    print(type(str1))
    print(type(json.loads(str1)))
    pass


def urllib_demo():
    """
    1.urllib.request.urlopen()——请求页面数据
    2.urllib.error——捕获url请求异常
    3.urllib.parse——url的各种解析、转码等操作
    4.urllib.request.urlopen()——做爬虫请求
    5.通过Request对象来构建请求
    :return:
    """
    # 案例1
    # response = urllib.request.urlopen('https://www.csdn.net/nav/python')  # GET请求
    # print(response.read().decode('utf-8'))

    # 案例2
    # try:
    #     response = urllib.request.urlopen('https://www.csdn.net/nav1/python')  # GET请求
    #     print(response.read().decode('utf-8'))
    # except urllib.error.HTTPError as e:
    #     print(e.code)

    # 案例3:urllib.parse
    # url_1 = 'http%3a%2f%2ftool.chinaz.com%2fTools%2furlencode.aspx'
    # url_2 = urllib.parse.unquote(url_1)
    # url_3 = urllib.parse.quote(url_2)

    # 案例4:urllib.request.urlopen(),POST请求
    # url_post = 'http://httpbin.org/post'
    # data = bytes(urllib.parse.urlencode({'tx': 'hello', 'sign': 'sdfjisd8126324dsfj'}), encoding='utf8')  # POST请求
    # response = urllib.request.urlopen(url=url_post, data=data)
    # print(response.read())

    # url_post = 'https://www.lanzous.com/filemoreajax.php'
    # data = bytes(urllib.parse.urlencode({'lx': 2, 'fid': 12583, 'uid': 85610, 'pg': 1, 'rep': '0', 't': 1575295545,
    #                                      'k': 'd616779d09c350dad2209569db36c322', 'up': 1}), encoding='utf8')  # POST请求
    # headers = {
    #     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', \
    #     'accept': 'application/json, text/javascript, */*',
    # }
    # response = urllib.request.urlopen(url=url_post, data=data, headers=headers)
    # print(response.read())

    # 案例5:
    url_post = 'https://www.lanzous.com/filemoreajax.php'
    data = bytes(urllib.parse.urlencode({'lx': 2, 'fid': 12583, 'uid': 85610, 'pg': 1, 'rep': '0', 't': 1575296284,
                                         'k': 'e7009279a6d3a43d126ede6be04aa24f', 'up': 1}), encoding='utf8')  # POST请求
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'accept': 'application/json, text/javascript, */*',
    }
    req = urllib.request.Request(url=url_post, data=data, headers=headers)
    response = urllib.request.urlopen(req)
    print(response.read())
    pass


def requests_demo():
    """
    pip install requests
    1.模拟进行requests的get和post请求
    2.response的一些参数
    response.status_code
    response.text
    response.content
    案例：b站番剧爬虫
    :return:
    """
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'accept': 'application/json, text/javascript, */*',
    }

    #知识点1： requests.get请求以及response.status_code、response.text、response.content、注意response.request的headers里面的ua
    # url_get = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1'
    # response = requests.get(url=url_get,headers = headers)
    # r_json = json.loads(response.text)

    # 知识点2：requests.post()请求
    # url_post = 'http://httpbin.org/post'
    # data ={'tx': 'hello', 'sign': 'sdfjisd8126324dsfj'}
    # response = requests.post(url=url_post, data=data,headers = headers)

    # 知识点3：response.text（str字符串型）和response.content的区别（bytes二进制型），案例：下载图片,使用文件读写的方式保存图片
    # response = requests.get('http://i0.hdslb.com/bfs/bangumi/f5d5f51b941c01f8b90b361b412dc75ecc2608d3.png',headers=headers)
    # with open('demo.jpg', 'wb+') as f:
    #     f.write(response.content)
    pass


def b_fanju_demo():
    """
    B站番剧爬虫demo
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'accept': 'application/json, text/javascript, */*',
    }
    # 1.确定数据来源：b站、番剧、需要的数据（封面、视频合集链接、视频当前更新集数、是否会员、追番人数、视频标题）
    # 2.确定抓取入口https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1
    # &copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1(需要分析数据各个请求参数)
    # 3.确定解析方式：json
    # 4.确定存储方式：txt文本
    url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=0&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize=20&type=1'
    for page in range(1, 10):
        response = requests.get(url=url.format(page = 1), headers=headers)
        dongman_list = json.loads(response.text)['data']['list']
        for item in dongman_list:
            thumb = item['cover']
            link = item['link']
            new_episode = int(re.findall('\d+', item['index_show'])[0])
            is_vip = 1 if item['badge'] else 0
            # 等价于以下写法
            # if item['badge']:
            #     is_vip = 0
            # else:
            #     is_vip = 0
            nums = item['order']
            title = item['title']
            with open('b站番剧.txt', 'a+') as f:
                f.write(json.dumps({'title':title, 'link':link,'new_episode':new_episode,'is_vip':is_vip,'nums':nums,'thumb':thumb,}))
    pass


if __name__ == '__main__':
    # json_demo()
    # urllib_demo()
    # requests_demo()
    b_fanju_demo()
