#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" 该模块实现对数据库进行增删改查 """

__author__ = "SSY"

import pymysql
import pymongo
import json



# 插入院士url
def insert_url(total, sum):
    # 获取数据库连接
    db = pymysql.connect("localhost", "root", "root", "paper")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 设置编码
    cursor.execute('set names utf8')
    # 设置自动提交
    cursor.execute('set autocommit = 1')  # 0:false   1:true

    for i in range(0, sum):
        print(total[i][0])
        print(total[i][1])
        sql = "replace INTO breed(id, name, url, popularity) VALUES ('{}', '{}', '{}', '{}');".format(total[i][1], total[i][3], total[i][2], total[i][0])
        # sql = "insert into academician (name, url) values('{0}','{1}')".format(total[i][1], total[i][0])
        cursor.execute(sql)
    print("插入成功，共计{0}条".format(sum))
    # 关闭数据库连接
    cursor.close()
    db.close()


# select院士
def select_all():
    # 获取数据库连接
    db = pymysql.connect("localhost", "root", "root", "paper")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    cursor.execute('set names utf8')
    cursor.execute('set autocommit = 1')  # 0:false   1:true
    sql = 'select id,url,name from breed'
    cursor.execute(sql)
    result = cursor.fetchall()
    print("获取成功，共计{0}条".format(len(result)))
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result


# 插入院士详情信息
def insert_detail(name, intro, photo):
    # 获取数据库连接
    db = pymysql.connect("localhost", "root", "root", "crawler")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    cursor.execute('set names utf8')
    cursor.execute('set autocommit = 1')  # 0:false   1:true

    sql = "insert into detail (name, intro, photo) values('{0}','{1}','{2}')".format(name, intro, photo)
    cursor.execute(sql)
    print("插入成功")
    # 关闭数据库连接
    cursor.close()
    db.close()

# 插入到Mongodb


def insert_mongodb():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    collection = paperdb["wheat1"]

    # x = collection.insert_many(items)
    with open('../data/ok.json', 'r', encoding="utf-8")as f:
        line = json.load(f)
        collection.insert(line)
        f.close()


def select_mongodb():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    with open("../data/ids.txt", "w", encoding="utf-8") as f:
        k = 0
        for x in col.find():
            if "bid" in x:
                print(x["bid"] + "   " + x["bname"])
                k = x["bid"]
            else:
                f.write(k + "\n")


def update_one_mongodb(bid):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    for x in col.find({"bid": str(bid)}):
        print(x["bid"] + "   " + x["bname"])
        col.update({'bid': str(bid)}, {'$set': {"bname": bname_process(x["bname"]) + ""}})


def is_double_str(s):
    res = str(s).replace('（', '').replace('）', '')
    if s[0:int(len(s)/2)] == s[int(len(s)/2):]:
        return True
    return False


def bname_process(s):
    res = str(s).replace('（', '').replace('）', '')
    return res[0:int(len(s)/2)]


def select():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    global t
    for x in col.find():
        if x is not None or x != "":
            print(type(x))
            if "bname" in x:
                x["bname"] = str(x["bname"]).replace('.', '').replace('⑴', '')
                if "（" in x["bname"]:
                    x["bname"] = x["bname"][:str(x["bname"]).index('（')]
                if is_double_str(x["bname"]):
                    x["bname"] = bname_process(x["bname"])
                if "一、" in x["bname"]:
                    x["bname"] = x["bname"][:str(x["bname"]).index('一、')]
                col.update({'bid': str(x["bid"])}, {'$set': {"bname": x["bname"]}})

