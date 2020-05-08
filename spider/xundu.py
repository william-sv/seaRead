# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/8 21:42
@Author    : William.sv@icloud.com
@File      : xundu.py
@ Software : PyCharm
@Desc      : 
"""

import requests
import random
import re
from urllib import parse
from bs4 import BeautifulSoup as bs
from util.requestUtil import user_agent

class Spider:
    def __init__(self):
        self.host = 'http://www.xundu.net/'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.xundu.net',
            'Pragma': 'no-cache',
            'User-Agent': user_agent()
        }
        self.session_resource = requests.session()
        self.session_resource.get(url=self.host, headers=self.headers)

    def search(self, **kwargs):
        keyword = kwargs['keyword']
        url_params = {
            'searchkey': keyword
        }
        url = parse.urljoin(self.host, 'search/result.html?' + parse.urlencode(url_params))
        r = self.session_resource.get(url=url)
        soup = bs(r.content, 'html5lib')
        data = soup.select('.pt-rank-detail > .pt-rank-detail-middle > .title > .mr60 > a')[0]
        fiction_url = data['href']
        fiction_name = data.string
        return {
            'fiction_url': fiction_url,
            'fiction_name': fiction_name
        }

    def pull_fiction(self):
        print()

    def pull_chatper(self, **kwargs):
        fiction_url = parse.urljoin(self.host, kwargs['fiction_url'])
        data = self.session_resource.get(url=fiction_url)
        soup = bs(data.content, 'html5lib')
        lists = soup.select('.pt-chapter-cont-detail > .compulsory-row-one')
        chapters = []
        for item in lists:
            chapter_url = item['href'].split('/')[-1].split('.')[0]
            chapter_name = item['title']
            chapters.append({
                'chapter_url': chapter_url,
                'chapter_name': chapter_name
            })
        return chapters

    def pull_chapter_content(self, **kwargs):
        chapter_url = parse.urljoin(self.host, kwargs['fiction_url'] + kwargs['chapter_url'] + '.html')
        data = self.session_resource.get(url=chapter_url)
        soup = bs(data.content, 'html5lib')
        chapter_content = soup.select('#content')[0]
        chapter_content = re.sub(r'<p>.*</p>', '', str(chapter_content))
        chapter_content = re.sub(r'<div id="content">', '', str(chapter_content))
        chapter_content = re.sub(r'</div>', '', str(chapter_content))
        return chapter_content


if __name__ == '__main__':
    keyword = '烂柯棋缘'
    # data = Spider().search(keyword=keyword)
    fiction_url = '/1602/'
    data = Spider().pull_chatper(fiction_url=fiction_url)
    print(data)
