#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/3/25 18:37
# @Author  : 504747754@qq.com(ZengYang)
# @File    : convers.py
# @Software: PyCharm
# @ToUse  :
import json
import traceback


def from_string_to_json(content):
    json_dict = {}
    try:
        json_dict = json.loads(content)
        json_dict = normalize_dict(json_dict)
    except Exception as e:
        traceback.print_exc()
    return json_dict


def from_json_to_string(data):
    data = normalize_dict(data)
    return json.dumps(data, ensure_ascii=False)


def normalize_dict(data):
    if type(data) == dict:
        new_data = {}
        for k in data:
            data[k] = normalize_dict(data[k])
            if type(k) == unicode:
                new_data[k.encode('utf-8')] = data[k]
            else:
                new_data[k] = data[k]
        data = new_data
    elif type(data) == list:
        for i in range(0, len(data)):
            data[i] = normalize_dict(data[i])
    elif type(data) == unicode:
        data = data.encode('utf-8')
    else:
        data = str(data)
    return data