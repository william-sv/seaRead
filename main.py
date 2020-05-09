# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/10 00:25
@Author    : William.sv@icloud.com
@File      : main.py
@ Software : PyCharm
@Desc      : 
"""

import time
import threading
from spider.xbiquege import Spider as xbiquege_spider
from spider.dingdianxs import Spider as dingdianxs_sipder

result = []


def search(keyword,tag):
    if tag == 'xbiquege':
        result.append(xbiquege_spider().search(keyword=keyword))
    if tag == 'dingdianxs':
        result.append(dingdianxs_sipder().search(keyword=keyword))


if __name__ == '__main__':
    keyword = '烂柯棋缘'
    thread1 = threading.Thread(target=search, args=(keyword,'xbiquege'))
    thread2 = threading.Thread(target=search, args=(keyword,'dingdianxs'))
    thread1.start()
    thread2.start()
    threads = [thread1, thread2]
    for t in threads:
        t.join()
    print(result)
    et = time.time()
