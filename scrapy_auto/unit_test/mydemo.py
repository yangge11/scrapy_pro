#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['FangSong']
plt.rcParams['axes.unicode_minus'] = False
# 设置图片大小
label = '超载', '船员责任心不强', '船员驾驶技术太差', '通航环境差', '海事、港航监管不到位', '船舶过于老旧', '冒险航行'  # 各类别标签
color = 'red', 'orange', 'yellow', 'green', 'blue', 'gray', 'goldenrod'  # 各类别颜色
size = [34, 5, 6, 14, 1, 10, 23]  # 各类别占比
explode = (0.2, 0, 0, 0, 0, 0, 0, 0)  # 各类别的偏移半径

pie = plt.pie(size, colors=color, explode=explode, labels=label, shadow=True, autopct='%1.1f%%')
# for digit in pie[2]:
#     digit.set_size(8)

plt.axis('equal')
plt.title('你认为砂石船发生事故的主要原因在于', fontsize=12)

plt.legend(loc=0, bbox_to_anchor=(0.82, 1))  # 图例
# 设置legend的字体大小
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=6)
plt.show()
pass
