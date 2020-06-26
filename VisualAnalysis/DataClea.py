# -*- coding: utf-8 -*-
# @Time : 2020/6/24 19:05 
# @Author : 永
# @File : DataAnalysis.py 
# @Software: PyCharm

import re

import pandas as pd

from db.MySql import SaveMysql
from jsondata.province_city import province_city

class DataClean(object):

    def __init__(self):
        self.mysql = SaveMysql()
        self.position_dcit = {}

    def run(self):
        self.get_position_data()

    def get_position_data(self):

        name = []   # 职位
        salary = []     # 薪资
        city = []       # 城市
        exprience = []  # 经验
        eduction = []   # 学历
        province = []
        data = self.mysql.get_data()
        for i in data:
            name.append(i[1])
            salary.append(i[2])
            city.append(i[3])
            exprience.append(i[4])
            eduction.append(i[5])
        # 把城市转换为省份
        data = province_city.keys()
        for i in data:
            citys = province_city[i]
            for j in citys:
                for k in city:
                    if k in j:
                        pro = i
                        province.append(pro)

        self.position_dcit["name"] = name
        self.position_dcit["salary"] = salary
        self.position_dcit["city"] = province
        self.position_dcit["exprience"] = exprience
        self.position_dcit["eduction"] = eduction

        # 拉勾网职位信息DataFrame
        df = pd.DataFrame(self.position_dcit)
        df.to_csv("D:\PythonFile\LagouSpider\imags\CsvFile\LagouPosition.csv")
        salary_low_list = []
        salary_high_list = []

        # 计算薪资(低薪和高薪)
        for x in salary:
            salary_low = float(re.findall(r"\d+",x)[0])
            salary_high = float(re.findall(r"\d+",x)[1])
            salary_low_list.append(salary_low)
            salary_high_list.append(salary_high)

        # 工作经验，低薪，高薪字典
        exprience_salary_dict = {
            "exprience":exprience,"salary_low":salary_low_list,"salary_high":salary_high_list
        }
        exprience_salary_df = pd.DataFrame(exprience_salary_dict)
        exprience_salary_df = exprience_salary_df[['exprience','salary_low','salary_high']].groupby('exprience').mean()
        exprience_salary_df.to_csv("D:\PythonFile\LagouSpider\imags\CsvFile\exprience_salary.csv")  # 存入csv文件
        # 工作城市，低薪，高薪字典
        city_salary_dict = {
            "city": city, "salary_low": salary_low_list, "salary_high": salary_high_list
        }
        city_salary_dict_df = pd.DataFrame(city_salary_dict)
        city_salary_dict_df = city_salary_dict_df[['city', 'salary_low', 'salary_high']].groupby(
            'city').mean()
        city_salary_dict_df.to_csv("D:\PythonFile\LagouSpider\imags\CsvFile\city_salary.csv")   # 存入csv文件

        # 学历，低薪，高薪字典
        eduction_salary_dict = {
            "eduction": eduction, "salary_low": salary_low_list, "salary_high": salary_high_list
        }
        eduction_salary_df = pd.DataFrame(eduction_salary_dict)
        eduction_salary_df = eduction_salary_df[['eduction', 'salary_low', 'salary_high']].groupby(
            'eduction').mean()
        eduction_salary_df.to_csv("D:\PythonFile\LagouSpider\imags\CsvFile\eduction_salary.csv")    # 存入csv文件

        # 低薪，高薪字典
        salary_dict = {
            "salary_low":salary_low_list,"salary_high":salary_high_list
        }
        salary_df = pd.DataFrame(salary_dict)
        salary_df.to_csv("D:\PythonFile\LagouSpider\imags\CsvFile\salary.csv")


if __name__ == '__main__':
    app = DataClean()
    app.run()