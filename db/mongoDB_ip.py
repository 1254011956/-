# -*- coding: utf-8 -*-
# @Time : 2020/5/25 18:23 
# @Author : 永
# @File : mongoDB_ip.py 
# @Software: PyCharm

import pymongo

from setting import MONGO_URL

class MongoPool(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URL)
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        self.client.close()
        
    def http(self):
        cursors = self.proxies.find({'score':50,'protocol':0})
        my_ip = []
        for cursor in cursors:
            ip = cursor['ip']
            port = cursor['port']
            ipp = ip + ':' + port
            my_ip.append(ipp)
        return my_ip
    
    def https(self):
        cursors = self.proxies.find({'score':50,'protocol':2})
        my_ip = []
        for cursor in cursors:
            ip = cursor['ip']
            port = cursor['port']
            ipp = ip + ':' + port
            my_ip.append(ipp)
        return my_ip

if __name__ == '__main__':
    pool = MongoPool()
    pool.http()