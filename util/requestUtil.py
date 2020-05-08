# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/8 21:47
@Author    : William.sv@icloud.com
@File      : requestUtil.py
@ Software : PyCharm
@Desc      : 
"""

import random


def user_agent():
    user_agent = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'
        ]
    return random.choice(user_agent)
