# -*- coding:utf-8 -*-

"""
本模块专门处理病虫害
"""

import pymongo
import re


def analyze_field():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    s = set()
    for x in col.find():
        for key in x:
            s.add(key)
    for p in s:
        print(p)


# 实验结果
# {'抗性鉴定': 51, '抗病性鉴定': 275,
# '抗病评价': 5, '抗病性': 7, '抗性表现': 88,
# '品质结果': 132, '抗旱鉴定': 14,
# '抗病性鉴定结果': 72, '抗病鉴定': 313, '抗性评价': 5}
def analyze_disease():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = {"抗性鉴定": 0,
             "抗病性鉴定": 0,
             "抗病评价": 0,
             "抗病性": 0,
             "抗性表现": 0,
             "品质结果": 0,
             "抗旱鉴定": 0,
             "抗病性鉴定结果": 0,
             "抗病鉴定": 0,
             "抗性评价": 0
             }
    for x in col.find():
        for key in count:
            if key in x:
                print(x[key])


#analyze_field()
analyze_disease()
