# -*- coding:utf-8 -*-

"""
将处理好的mongodb数据导入neo4j中
"""

from neo4j import GraphDatabase
import pymongo

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "root"))


def add_breed(tx, father, bname, bid):
    """
    match(f:Breed1{name:"冬性小麦"}) create (b:Breed1)-[r:belongs_to]->(f)
    """
    tx.run("match(f:" + type_name[father] + "{name:\"" + father + "\"}) create"
           "(b:" + type_name[father] + "{name:\"" + bname + "\",bid:" + bid + "})-[r:belong_to]->(f)")


def delete_relation(tx, name):
    """
    （p：Person  { 名称： “ Jennifer” } ） - [ rel：LIKES ] -> （g：Technology  { type： “ Graphs” } ）

    """
    tx.run("match (b:" + type_name[name] + "{name:\"" + name + "\"})-[r:belong_to]-(w:" + type_name[name] + ") delete r,w")


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])


type_name = {"半冬性小麦": "Breed2", "冬性小麦": "Breed1", "春性小麦": "Breed4",
             "弱春性小麦": "Breed5", "弱冬性小麦": "Breed3", "其它": "Breed6"}


def add_all_breed():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    with driver.session() as session:
        for x in col.find():
            if "btype" in x:
                session.write_transaction(add_breed, x["btype"], x["bname"], x["bid"])
                print(x["bid"] + "  success")
            else:
                print("Error: " + x["bid"] + " 不存在btype字段")


def test_delete():
    with driver.session() as session:
        for key in type_name:
            print(key)
            session.write_transaction(delete_relation, key)


relation_names = ["选育单位", "育种者", "育种人", "申请者", "申请人", "申请单位", "申请者"]


# 将组指机构加入到neo4j Graph上
def add_organization():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    paperdb = myclient["paper"]
    col = paperdb["wheat1"]
    # i = 0
    with driver.session() as session:
        for x in col.find():
            # if i != 7:
            #     i += 1
            #     continue
            for p in relation_names:
                if p in x:
                    items = str(x[p]).replace('。', 's').replace('.', '').replace('，', '-').replace(',', '-').replace('、', '-').split('-')
                    for k in items:
                        session.read_transaction(judge_has_node, k)
                        if is_exist_node:
                            session.write_transaction(add_relation_with_organization, k, type_name[x["btype"]], x["bid"], p)
                            print(x["bid"] + "--1--" + p)
                        else:
                            session.write_transaction(add_node, k, type_name[x["btype"]], x["bid"], p)
                            print(x["bid"] + "--2--" + p)


def add_node(tx, name, node_name, bid, relation_name):
    print("match (w:" + node_name + "{bid:" + bid + "})create (o:Organization{name:\"" + name + "\"})<-[:" + relation_name + "]-(w)")
    tx.run("match (w:" + node_name + "{bid:" + bid + "})create (o:Organization{name:\"" + name + "\"})<-[:" + relation_name + "]-(w)")


is_exist_node = False


def judge_has_node(tx, name):
    global is_exist_node
    if is_exist_node:
        is_exist_node = False
    print("match (w:Organization{name:\"" + name + "\"}) return w")
    result = tx.run("match (w:Organization{name:\"" + name + "\"}) return w")
    # print(len(result))
    for record in result:
        if len(record) != 0:
            is_exist_node = True
            break
        else:
            is_exist_node = False


def add_relation_with_organization(tx, name, node_name, bid, relation_name):
    tx.run(
        "match(w:" + node_name + "{bid:" + bid + "}) match(o:Organization{name:\"" + name + "\"}) create (o)<-[:" + relation_name + "]-(w)")


add_organization()