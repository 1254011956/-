# -*- coding: utf-8 -*-
# @Time : 2020/5/25 10:44 
# @Author : 永
# @File : lagouspider.py 
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests
from lxml import etree
import time
import random
import os

from setting import KEY
from util.log import logger
from util.USER_AGENT import get_user_agent
from db.mongoDB_ip import MongoPool
from db.MySql import SaveMysql

URL_PATH = "D:\PythonFile\LagouSpider/"

class LGSpider(object):
    urls = []
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.option.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(executable_path='D:\Python38\chromedriver.exe', options=self.option)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
        })
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser"}})
        self.url = 'https://www.lagou.com/'
        self.mongopool = MongoPool()



    def run(self):
        self.driver.get(url=self.url)
        time.sleep(1)
        try:
             WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,"//p[@class='checkTips']/a"))
            ).click()
        except:
            pass
        self.driver.find_element_by_id('search_input').send_keys(KEY)
        time.sleep(1)
        self.driver.find_element_by_class_name('search_button').click()
        try:
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"body-btn"))
            ).click()
        except:
            pass
        source = self.driver.page_source
        # self.parse_page(source)
        self.page_scroll()
        self.parse_url(self.urls)


    def get_url(self,source):

        html = etree.HTML(source)
        links = html.xpath("//ul/li//div[@class='p_top']/a/@href")
        for link in links:
            self.urls.append(link)

    def page_scroll(self):
        while True:
            next_Btn = WebDriverWait(driver=self.driver, timeout=5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))
            )
            if "pager_next_disabled" in next_Btn.get_attribute("class"):
                return 
            else:
                next_Btn.click()
                source = self.driver.page_source
                self.get_url(source)
                time.sleep(2)

    def parse_url(self,urls):
        for url in urls:
            s = requests.Session()
            HEADERS = {
                'User-Agent':get_user_agent(),
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.9'
            }
            response = s.get(url,headers=HEADERS)
            try:
                if response.status_code != 200 or '页面加载中' in response.content.decode('utf-8') or '防御伪造请求' in response.content.decode('utf-8'):
                    proxy = {
                        'http': 'http://' + random.choice(self.mongopool.http()),
                        'https:': 'https://' + random.choice(self.mongopool.https())
                    }
                    response = s.get(url,headers=HEADERS,proxies=proxy)
                    self.job_details(response)
                else:
                    self.job_details(response)
            except:
                print(url)
                print(response.status_code)
                print(response.content.decode('utf-8'))

            path = URL_PATH.__add__("Lagou").__add__("_").__add__("网址")
            if os.path.exists(path):
                os.rmdir(path)
            else:
                os.mkdir(path)
            name = url.split(".")[1]
            fb = open(path + "{}.html".format(name), mode='w', encoding='utf-8')
            fb.write(response.content.decode('utf-8'))
            print("创建完成")


    def job_details(self, response):
        html = etree.HTML(response.content.decode('utf-8'))
        name = html.xpath("//div[@class='position-content-l']//h1[@class='name']/text()")[0]
        salary = html.xpath("//dd[@class='job_request']//span[1]/text()")[0]
        city = html.xpath("//dd[@class='job_request']//span[2]/text()")[0]
        experience = html.xpath("//dd[@class='job_request']//span[3]/text()")[0]
        eduction = html.xpath("//dd[@class='job_request']//span[4]/text()")[0]
        character = html.xpath("//dd[@class='job_request']//span[5]/text()")[0]
        advantage = html.xpath("//dd[@class='job-advantage']/p/text()")[0]
        requirement = ''.join(html.xpath("//dd[@class='job_bt']/div[1]/p/text()"))
        job_url = response.url
        data = [name, salary, city, experience, eduction, character,advantage,requirement,job_url]
        self.save_to_mysql(data)
        logger.info('插入一条数据成功')
        
    def save_to_mysql(self,data):
        sql = SaveMysql()
        sql.insert_one(data)

        
if __name__ == '__main__':
    spider = LGSpider()
    spider.run()