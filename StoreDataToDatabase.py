from pymysql import *
from threading import Thread
import os
from CityCode import *
import datetime

from query import query_train_info

city_dict = {}
key_list = []
value_list = []
trip_date = ""
def insertData(conn):
    try:
        global key_list
        global value_list
        global trip_date
        cursor = conn.cursor()
        print(len(value_list))
        for item in value_list:
            url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s" % (
                trip_date, value_list[0], item, "ADULT")
            result_list = query_train_info(url,key_list,value_list)
            print(result_list)
            if len(result_list)>0:
                for item in result_list:
                    # for i in range(len(result_list)):
                    sql_command = 'insert into traines(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"   );'%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11])
                    print(sql_command)
                    cursor.execute(sql_command)
                    conn.commit()
        cursor.close()
    finally:
        if 'conn' in dir() and callable(conn) and conn.open:
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
    for key, value in city_dict.items():
        key_list.append(key)
        value_list.append(value)

def main():
    conn = connect(host='localhost', user="root", password='root', database='myDB', charset="utf8")
    initDate()
    insertData(conn)


if __name__ == '__main__':
    main()
# insert into trains(carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat)
#     values("G9537","成都东","内江北","17:53","18:33","00:40","18","有","--","--","--","--")