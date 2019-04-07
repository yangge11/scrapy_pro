#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/24 16:37
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : common_parser.py
# @Software: PyCharm
# @ToUse  :
import re


def del_html_attr(page_source):
    # todo:<!-- >注释标签的去除处理，\n\t的去除处理
    """
    需求：去掉多余属性，只保留部分特定属性
    新版本思路：
    针对每一个label
    <div class="aa">==><div>
    """
    labels = re.findall(r'<[^/][^>]*>', page_source)
    for label in labels:
        label_to_replace = label.replace(re.match('<[^\s]*[\s|>]', label).group(0), '').replace('>', '')
        label_to_be = label
        to_replace_attrs_data = re.split(
            'href\s*=\s*"[^"]*"|src\s*=\s*"[^"]*"|href\s*=\s*\'[^\']*\'|src\s*=\s*\'[^\']*\'', label_to_replace)
        for to_replace_attr in to_replace_attrs_data:
            if to_replace_attr.replace(' ', '') != '':  # 去除类似' '字符串替换
                label_to_be = label_to_be.replace(to_replace_attr, '')
        page_source = page_source.replace(label, label_to_be)
    return page_source


def get_CN_str(str):
    return re.sub(r'[A-Za-z0-9\!\%\[\]\,\。<>/.:\、"\，\？\=\s]', "", str)


if __name__ == '__main__':
    page_source = """
    <a class="heading-toc" id="myths-and-misconceptions-about-arthritis-can-interfere-with-treatment">
    </a> 
    <h3 id="mntl-sc-block_2-0-4" class="comp mntl-sc-list-item-title mntl-sc-block mntl-sc-block-heading"> 
    <span class="mntl-sc-block-heading__text"> Myths and Misconceptions About Arthritis Can Interfere With Treatment 
    </span>
     </h3>
    <div id="mntl-sc-block_2-0-5" class="comp mntl-sc-block mntl-sc-block-html"> 
    <li class="footer-links-item">
    <a href="https://mediakit.verywell.com/verywell-advertising/"
                                                 target="_blank" rel="noopener" data-component="footerLinks"
                                                 data-source="footerLinks" data-type="advertiseWithUs" data-ordinal="1">Advertise
    </a>
    </li>
    <li class="footer-links-item" style src='asasasa'>style
    <a
                        href="/legal#cookies"
                        data-component="footerLinks"
                        data-type="cookiePolicy"
                        data-ordinal="1"
                        data-source="footerLinks"
                >Cookie Policy
                </a>
                </li>
                <li class="footer-links-item">
    """
    aa = del_html_attr(page_source)
