# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '火车票查询.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
import os
import datetime
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem

from CityCode import readFile, readCode
# from MyMessageBox import MyWindow
from query import query_train_info

nowtime = datetime.datetime.now()
nowtime_str = str(nowtime)
nowtime_now = nowtime_str.split(" ")
trip_date = nowtime_now[0]
key_list = []
value_list = []
city_dict = {}



class MyTable(QTableWidget):
    """自定义的表格控件"""
    def __init__(self, parent=None):
        super(MyTable, self).__init__(parent)
        self.setColumnCount(12)
        self.setItem(0, 0, QTableWidgetItem(self.tr("车次")))
        self.setItem(0, 1, QTableWidgetItem(self.tr("出发站")))
        self.setItem(0, 2, QTableWidgetItem(self.tr("目的地")))
        self.setItem(0, 3, QTableWidgetItem(self.tr("出发时间")))
        self.setItem(0, 4, QTableWidgetItem(self.tr("到达时间")))
        self.setItem(0, 5, QTableWidgetItem(self.tr("消耗时间")))
        self.setItem(0, 6, QTableWidgetItem(self.tr("一等座")))
        self.setItem(0, 7, QTableWidgetItem(self.tr("二等座")))
        self.setItem(0, 8, QTableWidgetItem(self.tr("软卧")))
        self.setItem(0, 9, QTableWidgetItem(self.tr("硬卧")))
        self.setItem(0, 10, QTableWidgetItem(self.tr("硬座")))
        self.setItem(0, 11, QTableWidgetItem(self.tr("无座")))

class Ui_Form(object):
    def __init__(self):
        self.initDate()
    def setupUi(self, Form):
        Form.setObjectName("火车票查询")
        Form.resize(1300, 650)
        #普通票单选框
        self.radio_adult = QtWidgets.QRadioButton(Form)
        self.radio_adult.setGeometry(QtCore.QRect(680, 40, 61, 22))
        self.radio_adult.setObjectName("radio_adult")
        self.radio_adult.setChecked(True)
        #学生票单选框
        self.radio_student = QtWidgets.QRadioButton(Form)
        self.radio_student.setGeometry(QtCore.QRect(680, 90, 61, 22))
        self.radio_student.setObjectName("radio_student")
        #出发地的输入框
        self.from_station = QtWidgets.QLineEdit(Form)
        self.from_station.setGeometry(QtCore.QRect(0, 40, 113, 27))
        self.from_station.setObjectName("from_station")
        #目的地输入框
        self.to_station = QtWidgets.QLineEdit(Form)
        self.to_station.setGeometry(QtCore.QRect(0, 110, 113, 27))
        self.to_station.setObjectName("to_station")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 10, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 80, 67, 17))
        self.label_2.setObjectName("label_2")

        self.button_enter = QtWidgets.QPushButton(Form)
        self.button_enter.setGeometry(QtCore.QRect(790, 30, 91, 91))
        self.button_enter.setObjectName("button_enter")
        self.button_enter.clicked[bool].connect(self.getMessage)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(150, 0, 67, 16))
        self.label_3.setObjectName("label_3")
        #列表头信息
        self.detailTable = QTableWidget(Form)
        # self.detailTable.setHea
        self.detailTable.setColumnCount(12)
        self.detailTable.setHorizontalHeaderLabels(
            ["车次", "出发站", "目的地", "出发时间", "到达时间", "消耗时间", "一等座", "二等座", "软卧", "硬卧", "硬座", "无座"])
        self.detailTable.setGeometry(QtCore.QRect(35,250,1203,33))
        self.detailTable.geometry()

        #显示结果的list
        self.result_list = MyTable(Form)
        self.result_list.setGeometry(QtCore.QRect(10, 284, 1243, 341))
        self.result_list.setObjectName("result_list")
        self.result_list.geometry()
        self.result_list.setUpdatesEnabled(True)
        self.result_list.setColumnCount(12)

        #日历选择框
        self.calendar = QtWidgets.QCalendarWidget(Form)
        self.calendar.setGeometry(QtCore.QRect(140, 20, 481, 207))
        self.calendar.setObjectName("calendar")
        self.calendar.clicked[QDate].connect(self.showDate)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 150, 67, 17))
        self.label_4.setObjectName("label_4")
        #站点输入框
        self.station_query = QtWidgets.QLineEdit(Form)
        self.station_query.setGeometry(QtCore.QRect(0, 170, 113, 27))
        self.station_query.setObjectName("station_query")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "火车票查询"))
        self.radio_adult.setText(_translate("Form", "普通"))
        self.radio_student.setText(_translate("Form", "学生"))
        self.label.setText(_translate("Form", "出发地"))
        self.label_2.setText(_translate("Form", "目的地"))
        self.button_enter.setText(_translate("Form", "查询"))
        self.label_3.setText(_translate("Form", "出发时间"))
        self.label_4.setText(_translate("Form", "站点"))
        # self.result_list.

    def showDate(self,date):
        global trip_date
        """获取日历选择的结果并组装成适配的字符串返回"""
       # 周一1月1 2018  周三 1月 31 2018
        canlindardate = date.toString()
        data_list = canlindardate.split(" ")
        #月份
        monthfirst = data_list[1]
        mode = re.compile(r'\d+')
        monthNum = mode.findall(monthfirst)
        if int(monthNum[0])<10:
            #正则表达式后是列表
            month = "0"+monthNum[0]
        day = data_list[2]
        # print(data_list[3])
        year = data_list[3]
        trip_date = year+"-"+month+"-"+day

    def initDate(self):
        global city_dict
        global key_list
        global value_list
        file = "./file/城市代码.txt"
        city_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042"
        if os.path.exists(file):
            city_dict = eval(readFile(file))
        else:
            city_dict = readCode(file, city_url)
        for key, value in city_dict.items():
            key_list.append(key)
            value_list.append(value)
    def getMessage(self):
        global trip_date
        from_station = self.from_station.text()
        to_station = self.to_station.text()
        purpose_codes = ""
        if self.radio_adult.isChecked():
            purpose_codes = "ADULT"
        if self.radio_student.isChecked():
            purpose_codes = "0X00"
        if from_station in key_list and to_station in key_list and trip_date.strip()!="" and purpose_codes.strip()!="":
            from_station_code = city_dict[from_station]
            to_station_code = city_dict[to_station]
            query_url = self.getUrl(trip_date,from_station_code,to_station_code,purpose_codes)
            result_list_list = query_train_info(query_url,key_list,value_list)



            #打印查询结果
            print(result_list_list)
            self.result_list.setRowCount(len(result_list_list))
            for i in range(len(result_list_list)):
                for j in range(len(result_list_list[i])):
                    twi1 = QTableWidgetItem(result_list_list[i][j])
                    self.result_list.setItem(i, j, twi1)
        else:
            print("else ++++++++++++++++++++++++")
            if from_station not in key_list:
                print("输入的出发地不正确")
                msg_box = MyWindow()
                msg_box.msg("提示","您输入的出发点不存在,请确认后重新输入")
                msg_box.show()
            elif to_station not in key_list:
                msg_box = MyWindow()
                msg_box.msg("提示", "您输入的目的地不存在,请确认后重新输入")
                msg_box.show()
                # self.button_enter.clicked.connect(self.msg)
            elif trip_date.strip() == "":
                nowtime = datetime.datetime.now()
                nowtime_str = str(nowtime)
                nowtime_now = nowtime_str.split(" ")
                trip_date = nowtime_now[0]
                print(nowtime)
                self.button_enter.clicked.connect(self.msg)
            elif purpose_codes.strip() == "":
                self.msg("提醒", "请选择票的类型")
                self.button_enter.clicked.connect(self.msg)
            print(from_station+"================"+to_station)
    def getUrl(self,trip_date,city_from_code,city_to_code,purpose_codes):
        url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s"%(trip_date, city_from_code, city_to_code, purpose_codes)
        return url

    def msg(self,title,message):
        reply = QMessageBox.information(QMessageBox.Warning,"提示","信息有误",QMessageBox.Yes | QMessageBox.No)
        return reply
class MyWindow(QtWidgets.QWidget,Ui_Form):
    """自定义的MessageBox"""
    def __init__(self):
        super(MyWindow, self).__init__()
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setObjectName("myButton")
        # self.myButton.setText(text)
        self.myButton.clicked.connect(self.msg)

    def msg(self,title,message):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        title,
                                        message,
                                        QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)