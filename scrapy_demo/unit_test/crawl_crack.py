#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/2/20 17:24
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : crawl_crack.py
# @Software: PyCharm
# @ToUse  : 各种爬虫的反爬处理


# 滑块验证码处理
import time
import traceback

from selenium.webdriver import ActionChains


def move_slider(driver):
    while True:
        try:
            # 定位滑块元素
            slider = driver.find_element_by_xpath("//span[@id='nc_1_n1z']")
            track = get_track()
            move_to_gap(driver, slider, track)
            # 查看是否认证成功，获取text值
            while True:
                try:
                    text = driver.find_element_by_xpath("//span[@class='nc-lang-cnt']")
                    break
                except:
                    traceback.print_exc()
                    continue
            # 目前只碰到3种情况：成功（请在在下方输入验证码,请点击图）；无响应（请按住滑块拖动)；失败（哎呀，失败了，请刷新）
            if text.text.startswith(u'验证通过'):
                break
            elif text.text.startswith(u'哎呀，出错了，点击刷新再来一次'):
                driver.find_element_by_xpath("//span[@class='nc-lang-cnt']/a").click()
                pass
        except Exception as e:
            traceback.print_exc()
            time.sleep(5)


def get_track(distance=200):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    t = 0.9
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def move_to_gap(driver, slider, track):
    try:
        ActionChains(driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(driver).release().perform()
    except:
        traceback.print_exc()
