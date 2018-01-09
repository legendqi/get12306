# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '火车票查询.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
import os
# import requests
import re

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QStandardItemModel
# from PyQt5.QtGui import Qt.Orientation
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from CityCode import readFile, readCode
from query import query_train_info

trip_date = ""
key_list = []
value_list = []
city_dict = {}
class MyModel(QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self.hexdata = data
        print('__init__')

    def data(self, index, role=None):
        return self.hexdata[index.row()]

    def rowCount(self, parent=None):
        # print('rowCount')
        return len(self.hexdata)

    def roleNames(self):
        # print('roleNames')
        return 'lineData'

class Ui_Form(object):
    def __init__(self):
        self.initDate()
    def setupUi(self, Form):
        Form.setObjectName("火车票查询")
        # Form.setWindowTitle("火车票查询")
        Form.resize(1300, 650)
        #普通票单选框
        self.radio_adult = QtWidgets.QRadioButton(Form)
        self.radio_adult.setGeometry(QtCore.QRect(680, 40, 61, 22))
        self.radio_adult.setObjectName("radio_adult")
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
        self.detailTable.setGeometry(QtCore.QRect(10,250,1203,33))
        self.detailTable.geometry()

        #显示结果的list
        self.result_list = QtWidgets.QListView(Form)
        self.result_list.setGeometry(QtCore.QRect(10, 284, 1203, 341))
        self.result_list.setObjectName("result_list")
        self.result_list.geometry()
        self.result_list.setUpdatesEnabled(True)
        # self.list_mode = QStandardItemModel()
        # self.result_list.setModel(QAbstractItemModel=)
        # self.list_mode =QtWidgets.QListView.ListModel()
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
        # print(to_data)
        # return to_data

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
            result_list = query_train_info(query_url,key_list,value_list)


            mymodele = QListListModel(result_list)
            self.result_list.item
            self.result_list.setModel(mymodele)
            for item in result_list:
                print(item)
        else:
            print("else ++++++++++++++++++++++++")
            if from_station not in key_list:
                # self.msg("提醒","您输入的出发地不存在,请确认后重新输入").show()
                self.button_enter.clicked.connect(self.msg)
            if to_station not in key_list:
                # self.msg("提醒", "您输入的目的地不存在,请确认后重新输入").show()
                self.button_enter.clicked.connect(self.msg)
            if trip_date.strip() == "":
                # self.msg("提醒", "您选择的日期有误,请重新选择").show()
                self.button_enter.clicked.connect(self.msg)
            if purpose_codes.strip() == "":
                # self.msg("提醒", "请选择票的类型").show()
                self.button_enter.clicked.connect(self.msg)
            print(from_station+"================"+to_station)
    def getUrl(self,trip_date,city_from_code,city_to_code,purpose_codes):
        url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s" % (
        trip_date, city_from_code, city_to_code, purpose_codes)
        return url

    def msg(self,title,message):
        reply = QMessageBox.information(QMessageBox.Warning,"提示","信息有误",QMessageBox.Yes | QMessageBox.No)
        return reply


# from kbuttongroup import KButtonGroup
