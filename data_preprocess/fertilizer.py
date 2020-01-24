# -*- coding:utf-8 -*-

"""
将栽培中的肥料抽取出来
"""

import pymongo
import re


# 统计数据中有多少没有相关字段
def statistic_seed():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    len1 = 0
    for x in col.find():
        len1 += 1
        # if "栽培技术要点" not in x and "栽培要点" not in x:
        if "每亩基础苗" in x:
            count += 1
            print(x["每亩基础苗"])
        elif "每亩播量" in x:
            count += 1
            print(x["每亩播量"])
    print("共有{}条有, 总数为{}".format(count, len1))


# 从文本中抽取栽培数量
def extract_seed():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    len1 = 0
    with open("../data/analyze/seed.csv", "w", newline="", encoding="utf-8") as f:
        p = ""
        for x in col.find():
            item = []
            item.append(p)
            if "栽培技术要点" not in x and "栽培要点" not in x:
                len1 += 1
            elif "栽培技术要点" in x:
                p = re.search(r"(适宜播量每亩|基本苗以每亩|播(种)*量(为)*|基本苗(每亩)*(控制在)*(为)*(：)*|亩保苗)((\d+\.*\d*～*－*-*\d+\.*\d*)(kg|万|kg/亩|千克|公斤)+)", x["栽培技术要点"])
                if p is None:
                    print(x["栽培技术要点"])
                else:
                    # print(p.group())
                    # item.append(x["bid"])
                    deal_intermediate_data(col, p.group(), x["bid"])
                    count += 1
            elif "栽培要点" in x:
                p = re.search(r"(适宜播量每亩|基本苗以每亩|播(种)*量(为)*|基本苗(每亩)*(控制在)*(为)*(：)*|亩保苗)((\d+\.*\d*～*－*-*\d+\.*\d*)(kg|万|kg/亩|千克|公斤)+)", x["栽培要点"])
                if p is None:
                    print(x["栽培要点"])
                else:
                    # print(p.group())
                    deal_intermediate_data(col, p.group(), x["bid"])
                    count += 1
        print(count)



k1 = k2 = 0


def deal_intermediate_data(col, s, bid):
    global k1, k2
    p = re.search(r"(\d+\.*\d*～*－*-*\d+\.*\d*)(kg|万|kg/亩|千克|公斤)+", s)
    if "万" in p.group():
        col.update({"bid": bid}, {"$set": {"每亩基础苗": p.group().replace('～', '-').replace('－', '-')}})
        k1 += 1
    else:
        col.update({"bid": bid}, {"$set": {"每亩播量": p.group().replace('～', '-').replace('－', '-')}})
        k2 += 1


# 从文本中抽取亩产
def extract_yield():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    # 总数为1548
    1548
    for x in col.find():
        if "产量表现" in x:
            it = re.finditer(r"(平均产量|(平均)*亩产|平均公顷产量(为)*)(\d+\.*\d*)(kg/亩|kg|Kg|千克|公斤)", x["产量表现"])
            print("---------------------")
            col.update({"bid": x["bid"]}, {"$set": {"最高产量": get_max_number(it)}})
            print(get_max_number(it))
            count += 1
    print(count)


# 获得最高亩产
def get_max_number(it):
    maxx = 0.0
    global res
    for p in it:
        q = re.search(r"(\d+\.*\d*)", p.group())
        print(q.group())
        if float(q.group()) > maxx:
            maxx = float(q.group())
            res = p.group()
    return res


# 基本苗14～16万
# extract_fertilizer()
# print("{}基础苗，{}播量, totals:{}".format(k1, k2, k1+k2))
statistic_seed()
