# -*- coding: utf-8 -*-
# @Time : 2020/6/24 21:54
# @Author : 永
# @File : Plot.py
# @Software: PyCharm

from collections import Counter

from pyecharts.globals import ChartType

from jsondata.province_city import province_city
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pyecharts.charts import Map,Geo
from pyecharts import options as opt

class Plot(object):
    def __init__(self):
        plt.rcParams['font.sans-serif'] = 'simhei'
        plt.rcParams['axes.unicode_minus'] = False

    def plot(self):
        self.plot_ex_sl()
        self.plot_ec_sl()
        self.plot_ct_sl()


    def plot_ex_sl(self):
        ex_sl = pd.DataFrame(pd.read_csv("D:\PythonFile\LagouSpider\imags\CsvFile\exprience_salary.csv"))
        # 低薪
        salary_low =  np.array(ex_sl.salary_low)
        salary_low = salary_low.tolist()#list
        # 高薪
        salary_high = np.array(ex_sl.salary_high)
        salary_high = salary_high.tolist()  # list
        # 经验
        exprience = np.array(ex_sl.exprience)
        exprience = exprience.tolist()  # list

        len_index = np.array(ex_sl.index)
        len_index = len_index.tolist()

        bar1 = plt.bar(len_index,height=salary_low,width=0.4,color='c',label = '低薪')
        bar2 = plt.bar(list(map(lambda x:x+0.4,len_index)),height=salary_high,width=0.4,color='orange',label = '高薪')
        plt.xticks([index + 0.2 for index in len_index],exprience)
        plt.ylabel("薪资水平/单位：千(K)")
        plt.xlabel("工作经验")
        plt.title("Python开发工程师薪资")
        plt.legend()
        plt.savefig(fname="D:\PythonFile\LagouSpider\imags\CsvFile\Python开发工程师薪资-经验.png", figsize=[15, 10])

    def plot_ct_sl(self):
        ct_sl = pd.DataFrame(pd.read_csv("D:\PythonFile\LagouSpider\imags\CsvFile\city_salary.csv"))
        # 低薪
        salary_low =  np.array(ct_sl.salary_low)
        salary_low = salary_low.tolist()#list
        # 高薪
        salary_high = np.array(ct_sl.salary_high)
        salary_high = salary_high.tolist()  # list
        # 经验
        city = np.array(ct_sl.city)
        city = city.tolist()  # list

        len_index = np.array(ct_sl.index)
        len_index = len_index.tolist()

        bar1 = plt.bar(len_index,height=salary_low,width=0.4,color='c',)
        bar2 = plt.bar(list(map(lambda x:x+0.4,len_index)),height=salary_high,width=0.4,color='orange')
        plt.xticks([index + 0.2 for index in len_index],city)
        plt.xticks(rotation=270)
        plt.ylabel("薪资水平/单位：千(K)")
        plt.xlabel("工作城市")
        plt.title("Python开发工程师薪资")
        plt.legend()
        plt.savefig(fname="D:\PythonFile\LagouSpider\imags\CsvFile\Python开发工程师薪资-城市.png", figsize=[20, 10])

    def plot_ec_sl(self):
        ec_sl = pd.DataFrame(pd.read_csv("D:\PythonFile\LagouSpider\imags\CsvFile\eduction_salary.csv"))
        # 低薪
        salary_low =  np.array(ec_sl.salary_low)
        salary_low = salary_low.tolist()#list
        # 高薪
        salary_high = np.array(ec_sl.salary_high)
        salary_high = salary_high.tolist()  # list
        # 经验
        eduction = np.array(ec_sl.eduction)
        eduction = eduction.tolist()  # list

        len_index = np.array(ec_sl.index)
        len_index = len_index.tolist()

        plt.bar(len_index, height=salary_low, width=0.4, color='c', label='低薪')
        plt.bar(list(map(lambda x: x + 0.4, len_index)), height=salary_high, width=0.4, color='orange',
                       label='高薪')
        plt.xticks([index + 0.2 for index in len_index], eduction)
        plt.ylabel("薪资水平/单位：千(K)")
        plt.xlabel("工作经验")
        plt.title("Python开发工程师薪资")
        plt.legend()
        plt.savefig(fname="D:\PythonFile\LagouSpider\imags\CsvFile\Python开发工程师薪资-学历.png", figsize=[15, 10])

    def plot_salary_pie(self):
        fields = ["salary_low","salary_high"]
        df = pd.read_csv("D:\PythonFile\LagouSpider\imags\CsvFile\salary.csv",usecols=[1,2])
        # 低薪
        salary_low = np.array(df.salary_low)
        salary_low = list(salary_low.tolist())
        # 高薪
        salary_high = np.array(df.salary_high)
        salary_high = list(salary_high.tolist())

        low_list_less_5K = []
        low_list_5K_10K = []
        low_list_10K_15K = []
        low_list_15K_20K = []
        low_list_20K_30K = []
        low_qita = []
        for salary in salary_low:
            salary = int(salary)
            if salary < 5:
                low_list_less_5K.append(salary)
            elif salary >= 5 and salary < 10:
                low_list_5K_10K.append(salary)
            elif salary >= 10 and salary < 15:
                low_list_10K_15K.append(salary)
            elif salary >= 15 and salary < 20:
                low_list_15K_20K.append(salary)
            elif salary >=20 and salary < 30:
                low_list_20K_30K.append(salary)
            else:
                low_qita.append(salary)

        low_salary_len = [len(low_list_less_5K),len(low_list_5K_10K),len(low_list_10K_15K),
                          len(low_list_15K_20K),len(low_list_20K_30K),len(low_qita)]

        low_salary_name_detail = ["5K以下","5K-10K","10K-15K","15K-20K","20K-30K","30K以上"]
        explode = (0, 0, 0, 0.1, 0, 0)

        plt.pie(low_salary_len,explode=explode,labels=low_salary_name_detail,autopct='%1.2f%%',shadow=True,startangle=150,radius=1.3)
        plt.savefig("D:\PythonFile\LagouSpider\imags\CsvFile\Python开发工程师薪资分布详情.png",figsize=[15,10])

    def country_job_num(self):
        df = pd.read_csv("D:\PythonFile\LagouSpider\imags\CsvFile\LagouPosition.csv")
        citys = df.city
        count = Counter(citys)
        # count = count.most_common(len(count))
        city_list = []
        for city in count:
            city_list.append([city,count[city]])

        map = Geo()
        map.add_schema("china")
        map.add("geo",city_list,type_=ChartType.EFFECT_SCATTER)
        map.set_series_opts(label_opts=opt.LabelOpts(is_show=False))

        map.set_global_opts(
            visualmap_opts=opt.VisualMapOpts(),
            title_opts=opt.TitleOpts(title = "Python开发工程师分布情况"),
        )

        map.render(path="中国地图.html")
if __name__ == '__main__':
    app = Plot()
    app.country_job_num()