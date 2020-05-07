# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/7 22:32
@Author    : William.sv@icloud.com
@File      : xbiquege.py
@ Software : PyCharm
@Desc      : 
"""

import requests
import random
import re
from urllib import parse
from bs4 import BeautifulSoup as bs


class Spider:
    def __init__(self):
        self.host = 'http://www.xbiquge.la'
        self.user_agent = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.xbiquge.la',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(self.user_agent)
        }
        self.session_resource = requests.session()
        self.session_resource.get(url=self.host, headers=self.headers)

    def pull_fiction(self, **kwargs):
        fiction_data = {}
        keyword = kwargs['keyword']
        search_result = self.search(keyword=keyword)
        if search_result['fiction_name'] == '':
            print('未检索到 ' + keyword + ' 书籍！')
        chapters = self.pull_chatper(fiction_url=search_result['fiction_url'])
        fiction_data['name'] = search_result['fiction_name']
        fiction_data['fiction_url'] = search_result['fiction_url']
        fiction_data['chapters'] = chapters
        return fiction_data

    def pull_chatper(self, **kwargs):
        fiction_url = parse.urljoin(self.host, kwargs['fiction_url'])
        data = self.session_resource.get(url=fiction_url)
        soup = bs(data.content, 'html5lib')
        lists = soup.select('.box_con > #list > dl > dd')
        chapters = []
        for item in lists:
            tmp = item.contents[0]
            chapter_url = tmp['href'].split('/')[-1].split('.')[0]
            chapter_name = tmp.string
            chapters.append({
                'chapter_url': chapter_url,
                'chapter_name': chapter_name
            })
        return chapters

    def pull_chapter_content(self, **kwargs):
        chapter_url = parse.urljoin(self.host, kwargs['fiction_url'] + '/' +kwargs['chapter_url'] + '.html')
        print(chapter_url)
        data = self.session_resource.get(url=chapter_url)
        soup = bs(data.content, 'html5lib')
        chapter_content = soup.select('#content')[0]
        chapter_content = re.sub(r'<p>.*</p>', '', str(chapter_content))
        chapter_content = re.sub(r'<div id="content">', '', str(chapter_content))
        chapter_content = re.sub(r'</div>', '', str(chapter_content))
        return chapter_content

    def search(self, **kwargs):
        fiction_url = ''
        fiction_name = ''
        keyword = kwargs['keyword']
        url = 'http://www.xbiquge.la/modules/article/waps.php'
        post_data = {
            'searchkey': keyword
        }
        data = self.session_resource.post(url=url,data=post_data)
        soup = bs(data.content, 'html5lib')
        search_result = soup.select('.even')
        if len(search_result) > 0:
            fiction_url = parse.urlparse(search_result[0].contents[0]['href']).path
            fiction_name = search_result[0].contents[0].string

        return {
            'fiction_url': fiction_url,
            'fiction_name': fiction_name
        }


if __name__ == '__main__':
    fiction_url = '43/43943/'
    chapter_url = '19553404'
    # result = Spider().pull_chatper(fiction_url='43/43943/')
    # print(result)
    result = Spider().pull_fiction(keyword='绝对一番')
    print(result)
    # result = Spider().pull_chapter_content(fiction_url=fiction_url, chapter_url=chapter_url)
    # print(result)
