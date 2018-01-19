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
sichuan =  ["阿寨","埃岱","安德","安靖","广汉北","巴中",
    "白果",
    "白石岩",
    "百里峡",
    "柏村",
    "碑木镇",
    "彭山北",
    "苍溪",
    "朝天南",
    "成都",
    "达州",
    "大山铺",
    "大英东",
    "代湾",
    "德昌",
    "德阳",
    "都江堰",
    "渡市",
    "峨边",
    "峨眉",
    "峨眉山",
    "尔赛河",
    "甘洛",
    "共和",
    "关村坝",
    "广安",
    "广元",
    "红光镇",
    "汉源",
    "红峰",
    "花棚子",
    "华蓥",
    "简阳",
    "简阳南",
    "江油",
    "金口河",
    "敬梓场",
    "青城山",
    "开江",
    "孔滩",
    "拉白",
    "拉鲊",
    "阆中",
    "乐山",
    "乐武",
    "乐跃",
    "离堆公园",
    "李市镇",
    "联合乡",
    "凉红",
    "刘沟",
    "隆昌",
    "罗江东",
    "毛坝",
    "茅草坪",
    "眉山",
    "眉山东",
    "米易",
    "绵阳",
    "冕宁",
    "冕山",
    "内江",
    "南部",
    "南充",
    "南尔岗",
    "尼波",
    "尼日",
    "攀枝花",
    "彭州",
    "蓬安",
    "郫县",
    "郫县西",
    "平昌",
    "蒲坝",
    "普雄",
    "青白江东",
    "青莲",
    "青神",
    "渠县",
    "三汇镇",
    "沙马拉达",
    "沙湾",
    "上普雄",
    "双凤驿",
    "双流机场",
    "双流西",
    "苏雄",
    "遂宁",
    "铁口",
    "铁西",
    "桐子林",
    "土溪",
    "瓦祖",
    "弯坵",
    "万源",
    "王场",
    "武胜",
    "西昌",
    "犀浦",
    "喜德",
    "下普雄",
    "小儿坪",
    "谢家镇",
    "新都东",
    "新江",
    "新津",
    "新凉",
    "宣汉",
    "燕岗",
    "杨漩",
    "一步滩",
    "宜宾",
    "迤资",
    "迎宾路",
    "迎祥街",
    "营山",
    "永郎",
    "俞冲",
    "月华",
    "岳池",
    "越西",
    "枣子林",
    "轸溪",
    "竹园坝",
    "资阳",
    "资中",
    "自贡"]
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
                # print(result_list)
                for item in result_list:
                    # writer.writerow({'车次': item[0], '出发点': item[1],'目的地':item[2],'开车时间':item[3],'到达时间':item[4],'消耗时间':item[5],'一等座':item[6],'二等座':item[7],'软卧':item[8], '硬卧':item[9], '硬座':item[10], '无座':item[11]})
                    sql_command = 'insert into trainticks(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");'%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11])
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


def insertDataByTimeAndFromSttion(conn,cursor,from_station,starttime,endtime):
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
        starttime_float = float(starttime.replace(":","."))
        endtime_float = float(endtime.replace(":","."))
        print(len(value_list))
        for value_item in value_list:
            # print(value_item)
            url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s"%(trip_date, from_station, value_item, "ADULT")
            result_list = query_train_info(url,key_list,value_list)
            if len(result_list)>0:
                # print(result_list)
                for item in result_list:
                    item_float = float(item[3].replace(":", "."))
                    # print(str(starttime_float))
                    # print("startime" + str(starttime_float) + "===endtime" + str(endtime_float) + "====itemfloat" + str(
                    #     item_float))
                    # writer.writerow({'车次': item[0], '出发点': item[1],'目的地':item[2],'开车时间':item[3],'到达时间':item[4],'消耗时间':item[5],'一等座':item[6],'二等座':item[7],'软卧':item[8], '硬卧':item[9], '硬座':item[10], '无座':item[11]})
                    if ((item_float<=endtime_float) and (item_float >= starttime_float)):
                        print("startime" + str(starttime_float) + "===endtime" + str(
                            endtime_float) + "====itemfloat" + str(item_float))
                        sql_command = 'insert into trainticks(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");'%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11])
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


def insertDataByTimeAndToSttion(conn, cursor, to_station, starttime, endtime):
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
        starttime_float = float(starttime.replace(":", "."))
        endtime_float = float(endtime.replace(":", "."))
        print(len(value_list))
        for value_item in value_list:
            # print(value_item)
            url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s" % (
            trip_date, value_item, to_station, "ADULT")
            result_list = query_train_info(url, key_list, value_list)
            if len(result_list) > 0:
                # print(result_list)
                for item in result_list:
                    item_float = float(item[4].replace(":", "."))
                    # writer.writerow({'车次': item[0], '出发点': item[1],'目的地':item[2],'开车时间':item[3],'到达时间':item[4],'消耗时间':item[5],'一等座':item[6],'二等座':item[7],'软卧':item[8], '硬卧':item[9], '硬座':item[10], '无座':item[11]})
                    # print("startime" + str(starttime_float) + "===endtime" + str(endtime_float) + "====itemfloat" + str(
                    #     item_float))
                    if ((item_float <= endtime_float) and (item_float>=starttime_float)):
                        print("startime"+str(starttime_float)+"===endtime"+str(endtime_float)+"====itemfloat"+str(item_float))
                        sql_command = 'insert into trainticks(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");' % (
                        item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                        item[10], item[11])
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
    global sichuan
    # global conn
    # global cursor
    address = {'host':'localhost', 'user':"root", 'password':'root', 'database':'myDB', 'charset':"utf8"}
    # conn = connect(host='localhost', user="root", password='root', database='myDB', charset="utf8")
    # cursor = conn.cursor()
    # pool = PooledDB(**address)
    initDate()
    # sichuan_value = []
    # #new_value_list = value_list[:99]
    # for sichuan_item in sichuan:
    #     if sichuan_item in key_list:
    #         sichuan_value.append(city_dict[sichuan_item])
    # thread_list = []
    # for value_item in sichuan_value:
    #     thread = MyThread(value_item)
    #     thread_list.append(thread)
    #
    # for thread_item in thread_list:
    #     thread_item.start()
    #     print("线程开始")
    #     print(Thread.name)
    start_time = input("请输入开始的时间:")
    end_time = input("请输入结束的时间:")
    station = input("请输入要监控的站点:")
    conn1 = connect(**address)
    cursor1 = conn1.cursor()
    # def insertDataByTimeAndFromSttion(conn, cursor, from_station, starttime, endtime, station)
    from_thread = Thread(target=insertDataByTimeAndFromSttion,args=(conn1, cursor1,city_dict[station],start_time,end_time))
    from_thread.start()
    conn2 = connect(**address)
    cursor2 = conn2.cursor()
    # def insertDataByTimeAndToSttion(conn, cursor, to_station, starttime, endtime):
    to_thread = Thread(target=insertDataByTimeAndToSttion,args=(conn2,cursor2,city_dict[station],start_time,end_time))
    to_thread.start()

    # while True:
    #     print("子线程数量"+str(Thread.active_count()))
    #     sleep(1)
    # conn.close()
if __name__ == '__main__':
    main()
# insert into trains(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)
#     values("G9537","成都东","内江北","17:53","18:33","00:40","18","有","--","--","--","--")
