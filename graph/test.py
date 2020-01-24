# -*- coding:utf-8 -*-
import pymongo


def test_list():
    type_name = ["半冬性小麦", "冬性小麦", "春性小麦", "弱春性小麦", "弱冬性小麦"]
    x = "冬性小麦"

    if x in type_name:
        print("njhygyu")


def statistic_id():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    for x in col.find():
        if "审定编号" in x:
            count += 1
    print(count)


def test_author():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    for x in col.find():
        if "选育单位" in x:
            count += 1
            print(x["bid"] + " 选育单位 " + x["选育单位"])
        if "申请单位" in x:
            count += 1
            print(x["bid"] + " 申请单位 " + x["申请单位"])
        if "育种人" in x:
            count += 1
            print(x["bid"] + " 育种人 " + x["育种人"])
        if "育种者" in x:
            count += 1
            print(x["bid"] + " 育种者 " + x["育种者"])
        if "申请者" in x:
            count += 1
            print(x["bid"] + " 申请者 " + x["申请者"])
    print(count)


# 将整理好的机构更新到mongodb中
def update_organization():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    with open("../data/analyze/organization.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            items = line.replace('\r', '').replace('\n', '').replace('\t', '').split(" ")
            # col.update({'bid': str(x["bid"])}, {'$set': {"bname": x["bname"]}})
            col.update({"bid": str(items[0])}, {"$set": {"" + items[1]: items[2]}})
            print(items[0])


# 将选育者摘出
def update_col():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    for x in col.find():
        if "申请者" in x:
            if "选育者：" in str(x["申请者"]):
                items = str(x["申请者"]).split("选育者：")
                print(items[1])
                col.update({"bid": x["bid"]}, {"$set": {"申请者": items[0]}})
                print(x["bid"] + " 选育者 " + items[1])
                count += 1
    print(count)


test_author()