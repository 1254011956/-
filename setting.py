# -*- coding: utf-8 -*-
# @Time : 2020/5/25 10:39 
# @Author : 永
# @File : setting.py 
# @Software: PyCharm

import logging

# 日志配置信息
LOG_LEVEL = logging.DEBUG    #默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'    #默认格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'   #默认时间格式
LOG_FILENAME = 'log.log'    #默认日志文件名称

# Mysql配置信息
MYSQL = {
    'host':'localhost',
    'user':'root',
    'password':'123456',
    'database':'lagou',
    'charset':'utf8'
}

# 需要爬取数据的关键词
KEY = 'Python'

# MongoDB数据库的URL
MONGO_URL= 'mongodb://127.0.0.1:27017'