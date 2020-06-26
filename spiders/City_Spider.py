# -*- coding: utf-8 -*-
# @Time : 2020/6/25 22:43 
# @Author : 永
# @File : City_Spider.py 
# @Software: PyCharm

import requests
from lxml import etree
import re
import json

from collections import Counter

from util.USER_AGENT import get_user_agent

url = "https://www.fang.com/SoufunFamily.htm"

headers = {
    "User-Agent":get_user_agent()
}

response = requests.get(url,headers=headers)
html = etree.HTML(response.text)

# trs = html.xpath("//div[@class='outCont']//tr")
# # trs = html.xpath("//div[@class='outCont']//tr//td[not(class)]//strong/text()")
# city_list = []
# for tr in trs:
#     tds = tr.xpath(".//td[not(class)]")
#     province_td = tds[1]
#     province = province_td.xpath(".//strong/text()")
#     # if not province:
#     #     continue
#     # province1 = province[0]
#
#     city_td = tds[2]
#     city = city_td.xpath(".//a//text()")
#     city_list.append(city)
#     if not province:
#         continue
#
#
# print(city_list)

trs = html.xpath("//div[@class='outCont']//tr")

province_dict = {}

province = None
province_list = []
for tr in trs:
    tds = tr.xpath(".//td[not(@class)]")
    province_td = tds[0]
    province_text = None
    try:
        province_text = province_td.xpath(".//strong/text()")[0]
        province_text = re.sub('\s', '', str(province_text)).strip()
    except:
        pass
    if province_text:
        province = province_text
    if province == "其它":
        continue
    city_td = tds[1]
    city_links = city_td.xpath(".//a")
    city_list = []
    for city_link in city_links:
        city = city_link.xpath("./text()")[0]
        city_list.append(city)
    province_dict.setdefault(province,[]).append(city_list)
    # province_list.append(province_dict)

data =json.dumps(dict(province_dict),ensure_ascii=False)
fp = open("D:\PythonFile\LagouSpider\jsondata\province_city.json","w",encoding="utf-8")
fp.write(data+"\n")
fp.close()
