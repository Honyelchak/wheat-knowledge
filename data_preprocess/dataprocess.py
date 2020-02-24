# -*- coding:utf-8 -*-

"""
对小麦品种detail数据进行处理、存储
"""
__author__ = "JonnyYue"

import re

res = []

def process():
    with open("../data/items_after_process.txt", "r", encoding="utf-8") as f1, open("../data/set.txt", "r", encoding="utf-8") as f2:
        count = 0
        p = []
        # 将词典放到list列表中
        for word in f2.readlines():
            word_process = re.sub('(\s)*', '', word).replace('\n', '').replace('\r', '')
            p.append(word_process)

        for line in f1.readlines():
            # line_process = line.strip().replace(' ', '').rstrip().replace(' ', '').replace('\n', '').replace('\r', '')
            line_process = re.sub('(\s)*', '', line).replace("\"", "”")
            # print("start: " + line_process)
            for word1 in p:
                if word1 + ':' in line_process:
                    line_process = re.sub(word1 + ':', "\",\"" + word1 + "\":\"", line_process)
                    count = count + 1
                    # line_new = line_process.replace(word_process + ":", "\",\"" + word_process + "\":\"")
                elif word1 + '：' in line_process:
                    line_process = re.sub(word1 + '：', "\",\"" + word1 + "\":\"", line_process)
                    count = count + 1
            line_process = line_process + "\""
            line_process = re.sub('^(.*?)","', '{"', line_process, 1)
            line_process = line_process + "}"
            print(line_process)
            res.append(line_process)


# 部分数据(一条数据占据多行，该function功能为合并空行)


def data_clean():
    with open("../data/items.txt", "r", encoding="utf-8") as f1, open("../data/items_after_process.txt", "w", encoding="utf-8") as f2:
        for line in f1.readlines():
            item = re.search("^[\S]{3,}：[\S]{3,16}$", line)
            if item is None:
                f2.write(line.strip() + "\n")
            else:
                print(item.group())
                f2.write(item.group().strip().replace(' ', '').replace('\n', '').replace('\r', ''))
        f1.close()
        f2.close()


if __name__ == "__main__":
    #data_clean()
    process()
    f = False
    with open("../data/ok.txt", "w", encoding="utf-8") as f:
        for line in res:
            if not f:
                f = True
                f.write(line)
            else :
                f.write("," + line)
    #print(res)
    #dbutil.insert_mongodb(res)










