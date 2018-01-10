from CityCode import *
import requests
import os
city_dict = None
def main(from_station,to_station,trip_date,purpose_codes):
    global city_dict
    city_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042"
    file = "./file/城市代码.txt"
    if os.path.exists(file):
        city_dict = eval(readFile(file))
    else:
        city_dict = readCode(file,city_url)
    # from_station = input("请输入出发地城市名称:")
    # to_station = input("请输入目的地城市名称:")
    # trip_date = input("请输入出发时间格式为(xxxx-xx-xx):")
    # purpose_codes = input("请输入票的类型(ADULT/0X00,ADULT为普通票,0X00为学生票):")
    city_from_code = city_dict[from_station]
    city_to_code = city_dict[to_station]
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s"%(trip_date,city_from_code,city_to_code,purpose_codes)
    print(url)
    result_list = query_train_info(url)
    for item in result_list:
        print("=="*100)
        print(item)
def query_train_info(url,key_list,value_list):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''

    info_list = []
    try:
        r = requests.get(url, verify=False)
        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']
        if len(raw_trains)>0:
            for raw_train in raw_trains:
                # 循环遍历每辆列车的信息
                data_list = raw_train.split('|')
                # print(len(data_list))
                if len(data_list)>22:
                    # print(len(data_list))
                    # 车次号码
                    train_no = data_list[3]
                    # print("车次号码"+train_no)
                    # 出发站
                    from_station_code = data_list[6]
                    # print(from_station_code)
                    from_station_name = key_list[value_list.index(from_station_code)]
                    # print("出发地"+from_station_name)
                    # 终点站
                    to_station_code = data_list[7]
                    to_station_name = key_list[value_list.index(to_station_code)]
                    # 出发时间
                    start_time = data_list[8]
                    # 到达时间
                    arrive_time = data_list[9]
                    # 总耗时
                    time_fucked_up = data_list[10]
                    # print(time_fucked_up)
                    # 一等座
                    first_class_seat = data_list[31] or '--'
                    # 二等座
                    second_class_seat = data_list[30]or '--'
                    # 软卧
                    soft_sleep = data_list[23]or '--'
                    # 硬卧
                    hard_sleep = data_list[28]or '--'
                    # 硬座
                    hard_seat = data_list[29]or '--'
                    # 无座
                    no_seat = data_list[26]or '--'
                    # print(no_seat)
                    # 打印查询结果
                    info = [
                        train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
                        second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat]
                    info_list.append(info)

        return info_list
    except:
        return info_list
# if __name__ == '__main__':
#     main()

#https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-01-11&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=IEW&purpose_codes=ADULT
#https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-01-11&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=IEW&purpose_codes=ADULT