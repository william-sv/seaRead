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
from util.db import DB


class Fiction:
    def __init__(self):
        self.result = []

    def search(self, keyword, tag):
        if tag == 'xbiquege':
            self.result.append(xbiquege_spider().search(keyword=keyword))
        if tag == 'dingdianxs':
            self.result.append(dingdianxs_sipder().search(keyword=keyword))

    def run(self, keyword):
        thread1 = threading.Thread(
            target=self.search, args=(
                keyword, 'xbiquege'))
        thread2 = threading.Thread(
            target=self.search, args=(
                keyword, 'dingdianxs'))
        thread1.start()
        thread2.start()
        threads = [thread1, thread2]
        for t in threads:
            t.join()
        return self.result


if __name__ == '__main__':
    for item in ['烂柯棋缘','道长去哪了','射程之内遍地真理','绝对一番','我师兄实在太稳健了','大明望族','未来天王','绍宋','北宋大丈夫','氪金成仙','重生于康熙末年','官居一品','上品寒士','雅骚']:
        keyword = item
        result = Fiction().run(keyword)
        print(result)
        data = [result[0]['fiction_name'],result[0]['fiction_url'], str(int(time.time()))]
        table = 'fictions'
        columns = ['name','fiction_url','updated_at']
        DB().insert_once(data=data,columns=columns,table=table)
