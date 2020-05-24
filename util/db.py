# -*- coding: utf-8 -*-

"""
@Time      : 2020/5/24 14:59
@Author    : William.sv@icloud.com
@File      : db.py
@ Software : PyCharm
@Desc      :
"""

import time
import pymysql
from sercet_store.db_config import get_db_config


class DB:
    def __init__(self):
        db_config = get_db_config()
        self.host = db_config['host']
        self.user = db_config['user']
        self.password = db_config['password']
        self.database = db_config['database']
        self.db = None
        self.__conn()  # 连接数据库

    def __conn(self):
        try:
            self.db = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                use_unicode=True,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor)
            with self.db.cursor() as cursor:
                cursor.execute('SET NAMES utf8mb4;')
                cursor.execute('SET CHARACTER SET utf8mb4;')
                cursor.execute('SET character_set_connection=utf8mb4;')
                self.db.commit()
        except pymysql.err as e:
            print(e)

    def select(self, query, table):
        print()

    def update(self):
        print()

    def insert_once(self, **kwargs):
        data = kwargs['data']
        table = kwargs['table']
        columns = kwargs['columns']
        if len(data) != len(columns):
            raise Exception('插入列数与数据不一致，请检查后重试！')
        format_columns = ""
        format_data = ""
        for item in columns:
            format_columns += item + ','
        for item in data:
            format_data += ("'" + str(item) + "'") + ','
        format_columns = format_columns[:-1]
        format_data = format_data[:-1]
        sql = "INSERT INTO " + table + " (" + format_columns + ") VALUES (" + format_data + ")"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                self.db.commit()
        except pymysql.err as e:
            self.db.rollback()
            print(e)


if __name__ == '__main__':
    data = ['烂柯棋缘','真费事',1,'43/43943/', '1590308298']
    table = 'fictions'
    columns = ['name','author','source','fiction_url','updated_at']
    DB().insert_once(data=data,table=table,columns=columns)
