# -*- coding: utf-8 -*-
# @Time : 2020/5/25 10:38 
# @Author : 永
# @File : MySql.py 
# @Software: PyCharm

import pymysql

from setting import MYSQL

class SaveMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(**MYSQL)
        self.cursor = self.conn.cursor()
        self._sql = None

    def insert_one(self,data):
        self.cursor.execute(self.sql,data)
        self.conn.commit()
        self.conn.close()
    # def __del__(self):
    #     self.conn.close()

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into lagou_raw(id,name,salary,city,experience,eduction,charact,advantage,requirement,job_url) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            return self._sql
        return self._sql