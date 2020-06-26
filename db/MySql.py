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
        self._sql_get_data = None

    def __del__(self):
        self.conn.close()

    def insert_one(self,data):
        self.cursor.execute(self.sql,data)
        self.conn.commit()
        self.conn.close()

    def get_data(self):
        self.cursor.execute(self.sql_get_data)
        results = self.cursor.fetchall()
        return results

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into lagou_raw(id,name,salary,city,experience,eduction,charact,advantage,requirement,job_url) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            return self._sql
        return self._sql

    @property
    def sql_get_data(self):
        if not self._sql_get_data:
            self._sql_get_data = '''
                    select * from lagou_raw            
                    '''
            return self._sql_get_data
        return self._sql_get_data