# -*- coding:utf-8 -*-

import re
import csv
import pymongo


"""
将特征特性字段中的产量三要素提取出来

单位面积穗数
每穗粒数
千粒重
"""


vec = [79, 153]

rows = []


def getInfo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    count = 0
    for x in col.find():
        if x is not None or x != "":
            if "特征特性" in x:
                if int(x["bid"]) in vec:
                    continue
                # 单位面积穗数
                a = re.search(r"(平均)*亩*(成)*(有效)*(数)*穗(数)*(均匀)*(平均为)*(\d+(\.*\d+)±*－*—*-*/*\?*～*(\d+(\.*\d+))*)?万", str(x["特征特性"]))
                # 千粒重
                b = re.search(r"(千)*粒重(均匀|平均|约)*(\d+(\.*\d+)—*－*±*-*/*\?*～*(\d+(\.*\d+))*)?(克|g)", str(x["特征特性"]))
                # 每穗粒数
                c = re.search(r"(每穗粒数|每穗|结实粒数|穗粒数|结实)(均匀|平均)*(\d+(\.*\d+)—*±*－*-*/*\?*～*(\d+(\.*\d+))*)?(粒|个|，)", str(x["特征特性"]))
                item = []
                item.append(x["bid"])
                if a is None and b is None and c is None:
                    for i in range(0, 4):
                        item.append('0')
                elif a and b and c:
                    if a is not None:
                        item.append(deal_complex_str(a.group(8)))
                    if b is not None:
                        item.append(deal_complex_str(b.group(3)))
                    if c is not None:
                        p = re.search(r"(\d+(\.*\d+)—*±*－*-*/*\?*～*(\d+(\.*\d+))*)", c.group())
                        if p is None:
                            item.append(deal_complex_str(c.group()))
                        else:
                            item.append(deal_complex_str(p.group()))

                    item.append("{:.2f}".format(float(float(item[1])*float(item[2])*float(item[3])/100)))
                    if float(item[4]) < 400:
                        count += 1
                else:
                    if a is not None:
                        item.append(deal_complex_str(a.group(8)))
                    else:
                        item.append('0')
                    if b is not None:
                        item.append(deal_complex_str(b.group(3)))
                    else:
                        item.append('0')
                    if c is not None:
                        p = re.search(r"(\d+(\.*\d+)—*±*－*-*/*\?*～*(\d+(\.*\d+))*)", c.group())
                        if p is None:
                            # print(deal_complex_str(c.group()))
                            item.append(deal_complex_str(c.group()))
                        else:
                            # print(p.group())
                            item.append(deal_complex_str(p.group()))
                    else:
                        item.append('0')
                    item.append('0')
                print(item)
                tup = tuple(item)
                rows.append(tup)
    print(count)


csv_headers = ["bid", "单位面积穗数(万)", "千粒重(g)", "每穗粒数", "亩产量(kg)"]


def write_to_csv(headers, r):
    with open("../data/yield.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(r)


# 处理产量三要素中复杂的字符串
# — ± － - / \? ～[
def deal_complex_str(s):
    chars = ['—', '－', '-', '/', '?', '～']
    if str(s).find('±') != -1:
        p = s.split('±')
        # print(str(float(p[0])))
        return "{:.2f}".format(float(p[0]))
    for i in range(0, len(chars)):
        if chars[i] in s:
            p = s.split(chars[i])
            print(p)
            print(str((float(p[0]) + float(p[1]))/2))
            return str("{:.2f}".format((float(p[0]) + float(p[1]))/2))
    return s


"""
将理论产量计算出来
公式： "单位面积穗数(万)"x"千粒重(g)"x"每穗粒数"/100
"""


def getYield():
    cout = 0
    len1 = 0
    with open("../data/yield.csv", "r", encoding="utf-8") as f1:
        for line in f1.readlines():
            if len1 == 0:
                len1 += 1
                continue
            len1 += 1
            p = line.split(',')
            if float(p[4]) > 0:
                cout += 1
        print("有效品种为：{}, 有效产量为{}".format(len1, cout))


# getInfo()
# write_to_csv(csv_headers, rows)
# deal_complex_str("37.5～42.6")
# deal_complex_str("46/41")
# deal_complex_str("40/40")
# deal_complex_str("42.8～45.4")
# getYield()
getYield()