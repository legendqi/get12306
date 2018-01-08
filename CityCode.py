import requests
import re


def getCityCodeFromLine(url):
    """读取网页中的数据"""
    # 关闭https证书验证警告
    requests.packages.urllib3.disable_warnings()
    html = requests.get(url,verify=False)
    return html.text
def storeToFile(file,dict):
    """把数据处理之后储存到文件中"""
    file = open(file,"w")
    file.write(str(dict))
    file.close()
def readFile(file):
    """读取文件中的内容"""
    # if os.path.exists(self.file):
    file = open(file,"r")
    citycode = file.read()
    file.close()
    return citycode

def readCode(file,url):
    """处理数据储存为字典"""
    city_dict = {}
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    citycode = getCityCodeFromLine(url)
    result = re.findall(pattern, citycode)
    city_dict = dict(result)
    storeToFile(file,city_dict)
    return city_dict
    # city_list = citycode.split("=")[1].split("@")
    # for city in city_list:
    #     if "|" in city:
    #         city_item=city.split("|")
    #         city_dict[city_item[1]] = city_item[2]

# import requests
#
#
# #关闭https证书验证警告
# requests.packages.urllib3.disable_warnings()
# # 12306的城市名和城市代码js文件url
# url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
# r = requests.get(url,verify=False)
# pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
# result = re.findall(pattern,r.text)
# station = dict(result)