# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/7 22:32
@Author    : William.sv@icloud.com
@File      : xbiquege.py
@ Software : PyCharm
@Desc      : 
"""

import requests
import re
from urllib import parse
from bs4 import BeautifulSoup as bs
from util.requestUtil import user_agent


class Spider:
    def __init__(self):
        self.host = 'http://www.dingdianxs.com/'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.dingdianxs.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent()
        }
        self.session_resource = requests.session()
        self.session_resource.get(url=self.host, headers=self.headers)

    def pull_fiction(self, **kwargs):
        fiction_data = {}
        fiction_url = kwargs['fiction_url']
        chapters = self.pull_chatper(fiction_url=fiction_url)
        fiction_data['fiction_url'] = fiction_url
        fiction_info = self.pull_fiction_info(fiction_url=fiction_url)
        fiction_data['name'] = fiction_info['name']
        fiction_data['fiction_url'] = fiction_url
        fiction_data['cover'] = fiction_info['cover']
        fiction_data['author'] = fiction_info['author']
        fiction_data['intro'] = fiction_info['intro']
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

    def pull_fiction_info(self, **kwargs):
        fiction_url = parse.urljoin(self.host, kwargs['fiction_url'])
        data = self.session_resource.get(url=fiction_url)
        soup = bs(data.content, 'html5lib')
        fiction_id = kwargs['fiction_url'].split('/')[1]
        cover = self.host + '/files/article/image/' + kwargs['fiction_url'] + fiction_id + '.jpg'
        name = soup.select('#maininfo > #info > h1')[0].string
        author = soup.select('#maininfo > #info > p')[0].string.split('：')[1]
        intro = soup.select('#maininfo > #info > #intro')[0]
        intro = re.sub(r'<a.*</a>', '', str(intro))
        intro = re.sub(r'<br/>', '', str(intro))
        intro = re.sub(r'<div id="intro">', '', str(intro))
        intro = re.sub(r'</div>', '', str(intro))
        intro = re.sub(r'\s', '', str(intro))
        # intro = unicodedata.normalize('NFKC', str(intro))
        return {
            'name': name,
            'cover': cover,
            'author': author,
            'intro': intro
        }

    def pull_chapter_content(self, **kwargs):
        chapter_url = parse.urljoin(self.host, kwargs['fiction_url'] + '/' +kwargs['chapter_url'] + '.html')
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
        last_chapter = ''
        keyword = kwargs['keyword']
        url_params = {
            'searchkey': keyword
        }
        url = parse.urljoin(self.host, '/modules/article/search.php?' + parse.urlencode(url_params))
        data = self.session_resource.get(url=url)
        soup = bs(data.content, 'html5lib')
        if len(soup.select('.novelslistss > li')) > 0:
            tmp_ele = soup.select('.novelslistss > li')[0]
            fiction_info_ele = tmp_ele.select('span')
            fiction_url = fiction_info_ele[1].select('a')[0]['href']
            fiction_name = fiction_info_ele[1].select('a')[0].string
            last_chapter = fiction_info_ele[2].select('a')[0].string
        return {
            'fiction_url': fiction_url,
            'fiction_name': fiction_name,
            'last_chapter': last_chapter
        }


# test
if __name__ == '__main__':
    fiction_url = '52/52833/'
    # result = Spider().pull_fiction(fiction_url=fiction_url)
    result = Spider().search(keyword='绝对一番')
    print(result)
