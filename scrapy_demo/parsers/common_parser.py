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
    # # 指定属性方式去除，旧版本
    # to_del_attrs = [
    #     'class', 'id', 'data-role', 'style', 'target', 'title', 'alt', 'name', 'color', 'align', 'width',
    #     'height', 'appendurl', 'orgsrc', 'data-role', 'data-height', 'data-component', 'data-source', 'data-type',
    #     'data-ordinal', 'data-pos', 'data-priority', 'data-sizes', 'data-targeting', 'data-rtb', 'data',
    # ]
    # to_del_attrs = [
    #     'class', 'id', 'data-role', 'style', 'target', 'title', 'alt', 'name', 'color', 'align', 'width',
    #     'height', 'appendurl', 'orgsrc', 'data',
    # ]
    # # 查找带data-.*属性，并且进行替换,防止替换正文
    # to_replace_attrs_data = re.findall(r'data-[a-zA-Z|-]*\s*=\s*"[^"]*"', page_source)  # data-[a-zA-Z] = "aaa"
    # to_replace_attrs_data_extra = re.findall(r"data-[a-zA-Z|-]*\s*=\s*'[^']*'", page_source)  # data-[a-zA-Z] = 'aaa'
    # to_replace_attrs_data.extend(to_replace_attrs_data_extra)
    # for to_replace_attr in to_replace_attrs_data:
    #     page_source = page_source.replace(to_replace_attr, '')
    # # # example:view-source:https://www.verywellhealth.com/arthritis-10-important-facts-you-should-know-189663
    # # to_del_attrs_no_value = ['data-parent']
    # # for to_del_attr_no_value in to_del_attrs_no_value:
    # #     page_source = page_source.replace(to_del_attr_no_value, '')
    #
    # for to_del_attr in to_del_attrs:
    #     to_replace_attrs = re.findall(r'{to_del_attr}\s*=\s*"[^"]*"'.format(to_del_attr=to_del_attr),
    #                                   page_source)  # class="aaa"
    #     to_replace_attrs_extra = re.findall(r"{to_del_attr}\s*=\s*'[^']*'".format(to_del_attr=to_del_attr),
    #                                         page_source)  # class='aaa'
    #     to_replace_attrs.extend(to_replace_attrs_extra)
    #     for to_replace_attr in to_replace_attrs:
    #         page_source = page_source.replace(to_replace_attr, '')

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
    </a> <h3 id="mntl-sc-block_2-0-4" class="comp mntl-sc-list-item-title mntl-sc-block mntl-sc-block-heading"> 
    <span class="mntl-sc-block-heading__text"> Myths and Misconceptions About Arthritis Can Interfere With Treatment </span> </h3>
    <div id="mntl-sc-block_2-0-5" class="comp mntl-sc-block mntl-sc-block-html"> <li class="footer-links-item"><a href="https://mediakit.verywell.com/verywell-advertising/"
                                                 target="_blank" rel="noopener" data-component="footerLinks"
                                                 data-source="footerLinks" data-type="advertiseWithUs" data-ordinal="1">Advertise</a>
                </li>
                <li class="footer-links-item" style>style<a
                        href="/legal#cookies"
                        data-component="footerLinks"
                        data-type="cookiePolicy"
                        data-ordinal="1"
                        data-source="footerLinks"
                >Cookie Policy</a></li>
                <li class="footer-links-item">
    """
    aa = del_html_attr(page_source)
    pass
