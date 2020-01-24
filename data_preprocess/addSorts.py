# -*- coding:utf-8 -*-

import pymongo

"""
将mongodb中的数据添加一个类别字段(半冬性、弱冬性)
"""

file_name_list = ["bandongxing.txt", "dongxing.txt", "chunxing.txt", "ruochunxing.txt", "ruodongxing.txt"]
type_name = ["半冬性小麦", "冬性小麦", "春性小麦", "弱春性小麦", "弱冬性小麦"]


# 添加属性
def addproperty():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    for i in range(0, len(file_name_list)):
        items = []
        with open("../data/sort/"+file_name_list[i], "r", encoding="utf-8") as f:
            for line in f.readlines():
                items.append(line.replace('\r', '').replace('\n', '').replace('\t', ''))
            for x in col.find():
                if "bname" in x:
                    if x["bname"] in items:
                        col.update({'bid': x["bid"]}, {'$set': {"btype": type_name[i]}})
                        print(x["bid"] + "   success")
            f.close()


# 为文件中没有的添加属性(其他)
def addotherproperty():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    s = ""
    for x in col.find():
        if "btype" not in x:
            if "bid" not in x:
                print(s)
            else:
                col.update({"bid": x["bid"]}, {"$set": {"btype": "其它"}})
                s = x["bid"]


def analyze_btype():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    for x in col.find():
        if "btype" in x:
            if x["btype"] == "其它":
                count += 1
    print(count)


analyze_btype()