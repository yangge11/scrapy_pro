#!/usr/bin/python
# @Time    : 2019/12/1 18:58
# @Author  : 504747754@qq.com(ZengYang)
# @File    : demo.py
# @Software: PyCharm
# @ToUse  :
import json


def json_demo():
    dict1 = {"url": "https://www.lanzous.com/b12583", "name": "精品广场舞83-2.zip精品广场舞83-1.zip"}
    str1 = json.dumps(dict1)
    print(type(str1))
    print(type(json.loads(str1)))
    pass


if __name__ == '__main__':
    json_demo()
