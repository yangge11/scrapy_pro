#!/usr/bin/python
# @Time    : 2019/12/1 18:58
# @Author  : 504747754@qq.com(ZengYang)
# @File    : demo.py
# @Software: PyCharm
# @ToUse  :
import json
import urllib


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


if __name__ == '__main__':
    # json_demo()
    urllib_demo()
