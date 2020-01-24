#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs

""" 该模块实现对小麦信息的爬取 """

__author__ = "JonnyYue"

import requests
import re
from data_preprocess import dbutil

# 爬取链接
main_url = "https://www.chinaseed114.com/seed/xiaomai/"

# headers 请求头
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "UM_distinctid=16f4cfc0bea4a2-093e9164249d4-b363e65-13c680-16f4cfc0beb6bd; CNZZDATA1263499=cnzz_eid%3D1138656655-1577541562-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1578121912; Hm_lvt_af30b88003a23c39ae796a1ec0d18d5b=1577544584,1578043345,1578123952; PHPSESSID=3cf8c6cd3f01ae5284557358c2f06714; Hm_lpvt_af30b88003a23c39ae796a1ec0d18d5b=1578125450",
    "Host": "www.chinaseed114.com",
    "If-Modified-Since": "Sat, 04 Jan 2020 07:23:22 GMT",
    "If-None-Match": "40000000ce392-95fd-59b4b4d2795d7",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}


# 模拟浏览器请求获取网站html文件
def get_html(vid, url, name, headers):
    # 请求url
    req = requests.get(url, headers=headers)
    # 获取响应码
    code = req.status_code
    print("请求状态：{0}".format(code))
    html = req.text
    # print(html)
    html = html.encode('iso-8859-1').decode('utf-8')

    return [vid, html, name, url]


# 解析获取到的html代码(小麦品种网中具体的小麦品种)
def analysis_total_page(html):

    p = re.findall('<li class=\'t_c\'><span class="f_r f_light px12">(.*?)</span><span class="f_green px12 f_l"> (.*?)</span> <a href="(.*?)" target="_blank" class="px14" title="(.*?)">(.*?)</a></li>', html)
    print("个数：{0}".format(len(p)))

    for i in range(0, len(p)):
        print(p[i])
    return list(p)


# 解析获取到的html代码(单个detail的详情页)
def analysis_detail_page(html):
    # 获取院士资料
    # searchObj = re.search('<B>品质分析：</B>(.*?)<B>', html, re.S)


    c = re.sub('<[^<]+?>', '', str).replace('\n', '').strip()

    # if searchObj:
    #     # print(searchObj.group())
    #     print(searchObj.group(1))
    #     # print("searchObj.group(2) : {}", searchObj.group(2))
    # else:
    #     print("Nothing found!!")


def bs_fun(base_html):
    soup = bs(base_html[1], 'lxml')

    title = soup.select_one("#content")
    str1 = title.text
    m = {}
    with open("../data/set.txt", "r", encoding="utf-8") as f1, open("../data/items.txt", "a", encoding="utf-8") as f2:
        c = re.sub('<[^<]+?>', '', str1).replace('\n', '').strip().replace(' ', '')
        f2.write("burl:" + base_html[3] + "bid:" + str(base_html[0]) + "bname:" + base_html[2] + c + "\n")
        p = c.split('：')
        for i in range(len(p)):
            for line in f1.readlines():
                if p[i].find(line) > 0:
                    m[line] = p[i].replace(line, ' ').strip()
                    print(line, "  ", m[line])
        f1.close()
        f2.close()
    return m
# def bs_funtion(base_html):
#     soup = bs(base_html, 'lxml');
#
#     # print(soup)
#
#     title = soup.select("#article > div")
#
#     for i in title:
#         try:
#             title = i.select_one("b > span").text
#             ppp.add(title)
#             # print(title)
#             commentAll = i.children
#             commentAll.__next__();
#
#             comment = ''
#             for j in commentAll:
#                 comment += j.text
#             print([title,comment])
#         except BaseException:
#             print("error  {}".format(i))


# 解析冬小麦、半东性小麦...(存入txt文件中)
def getSort(html):
    p = re.findall('<li class=\'t_c\'><span class="f_r f_light px12">(.*?)</span><span class="f_green px12 f_l"> (.*?)</span> <a href="(.*?)" target="_blank" class="px14" title="(.*?)">(.*?)</a></li>',
        html)
    print("个数：{0}".format(len(p)))
    with open("../data/sort/ruodongxing.txt", "a", encoding="utf-8") as f:
        for i in range(0, len(p)):
            f.write(p[i][3] + "\n")
            print(p[i][3])
        f.close()
    return list(p)


    # --------- 下面是存储所有小麦品种url的信息
    # for i in range(21):
    #     html = get_html(main_url + str(i+1) + ".html", header)
    #     s = analysis_total_page(html)
    #     dbutil.insert_url(s, len(s))

    # ----------- 下面是存储院士详情页信息代码

    # 从数据库获取所有院士的链接
    # all = dbutil.select_all()
    # # 遍历每个院士的链接
    # # for i in range(0, len(all)):
    # print(all[0])
    # # 爬取单个院士的详情页
    # html = get_html(all[0][1], header)
    # print(html)
    # # 解析单个院士详情页
    # analysis_detail_page(html)
        # print(detail)
        # # 将详情页中的信息保存到数据库
        # dbutil.insert_detail(all[i][2], detail[0].replace('\'', '"'), detail[1])
    # all = dbutil.select_all()
    # for i in range(0, len(all)):  # 具体网址   all[i][1]
    #     k = bs_fun(get_html(all[i][0], all[i][1], all[i][2], header))
    #     # soup = bs(all[i][1], 'lxml');
    # for key, value in k.items():
    #     print(key + ':' + value)


if __name__ == '__main__':
    for i in range(1, 2):
        main_url = "https://www.chinaseed114.com/seed/141/" + str(i) + ".html"
        p = get_html(137, main_url, "冬性小麦", header)
        getSort(p[1])
