# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/10 00:25
@Author    : William.sv@icloud.com
@File      : main.py
@ Software : PyCharm
@Desc      : 
"""

from spider.xbiquege import Spider as xbiquege_spider
from spider.dingdianxs import Spider as dingdianxs_sipder


def search(keyword):
    result = {'xbiquege': xbiquege_spider().search(keyword=keyword),
              'dingdianxs': dingdianxs_sipder().search(keyword=keyword)}
    return result


if __name__ == '__main__':
    keyword = '烂柯棋缘'
    result = search(keyword)
    print(result)