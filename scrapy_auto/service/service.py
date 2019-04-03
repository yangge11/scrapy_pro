#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/3/20 14:49
# @Author  : 504747754@qq.com(ZengYang)
# @File    : service.py
# @Software: PyCharm
# @ToUse  : 数据可视化service
from flask import Flask, render_template, app

app = Flask(__name__)


@app.route('/index', methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1080, debug=True)
