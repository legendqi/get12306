import csv
from time import sleep

import pymysql
from DBUtils import PooledDB
from pymysql import *
from threading import Thread
import os
from CityCode import *
import datetime

from query import query_train_info
address = {}
city_dict = {}
key_list = []
value_list = []
trip_date = ""
class MyThread(Thread):
    def __init__(self,from_station):
        Thread.__init__(self)
        self.from_station = from_station

    def run(self):
        conn = connect(**address)
        cursor = conn.cursor()
        insertData(conn,cursor,self.from_station)

def insertData(conn,cursor,from_station):
    try:
        global key_list
        global value_list
        global trip_date
        cursor = conn.cursor()
        # file = open('./file/names.csv', 'w')
        # fieldnames = ['车次', '出发点', '目的地', '开车时间', '到达时间', '消耗时间', '一等座',
        #               '二等座', '软卧', '硬卧', '硬座', '无座']
        # writer = csv.DictWriter(file, fieldnames=fieldnames)
        # writer.writeheader()
        print(len(value_list))
        for value_item in value_list:
            # print(value_item)
            url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s"%(trip_date, from_station, value_item, "ADULT")
            result_list = query_train_info(url,key_list,value_list)
            if len(result_list)>0:
                print(result_list)
                for item in result_list:
                    # writer.writerow({'车次': item[0], '出发点': item[1],'目的地':item[2],'开车时间':item[3],'到达时间':item[4],'消耗时间':item[5],'一等座':item[6],'二等座':item[7],'软卧':item[8], '硬卧':item[9], '硬座':item[10], '无座':item[11]})
                    sql_command = 'insert into traines(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");'%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11])
                    print(sql_command)
                    try:
                        result = cursor.execute(sql_command)
                        insert_id = conn.insert_id()
                        conn.commit()
                        if result:
                            print("插入成功", insert_id)
                    except pymysql.Error as e:
                        print("发生异常，无法插入数据")
                        conn.rollback()
                        # 主键唯一，无法插入
                        if "key 'PRIMARY'" in e.args[1]:
                            print("数据已存在，未插入数据")
                        else:
                            print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
                result_list = []


    finally:
        if 'conn' in dir() and callable(conn) and conn.open:
            cursor.close()
            conn.close()
            print("closed successfully.")
def initDate():
    global city_dict
    global key_list
    global value_list
    global trip_date
    nowtime = datetime.datetime.now()
    nowtime_str = str(nowtime)
    nowtime_now = nowtime_str.split(" ")
    trip_date = nowtime_now[0]
    file = "./file/城市代码.txt"
    city_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042"
    if os.path.exists(file):
        city_dict = eval(readFile(file))
    else:
        city_dict = readCode(file, city_url)

    print("字典的长度"+str(len(city_dict)))
    for key, value in city_dict.items():
        key_list.append(key)
        value_list.append(value)


    # key_set = set(value_list)
    # for item in key_set:
    #     if value_list.count(item)>1:
    #         print("the %s has found %d"%(item,value_list.count(item)))
    #     else:
    #         print("+++++++++++++++++++++++")

def main():
    global address
    # global conn
    # global cursor
    address = {'host':'localhost', 'user':"root", 'password':'root', 'database':'myDB', 'charset':"utf8"}
    # conn = connect(host='localhost', user="root", password='root', database='myDB', charset="utf8")
    # cursor = conn.cursor()
    pool = PooledDB(**address)
    initDate()
    #new_value_list = value_list[:99]
    thread_list = []
    for value_item in value_list:
        thread = MyThread(value_item)
        thread_list.append(thread)

    for thread_item in thread_list:
        thread_item.start()
        print("线程开始")
        print(Thread.name)

    # while True:
    #     print("子线程数量"+str(Thread.active_count()))
    #     sleep(1)
    # conn.close()
if __name__ == '__main__':
    main()
# insert into trains(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)
#     values("G9537","成都东","内江北","17:53","18:33","00:40","18","有","--","--","--","--")
