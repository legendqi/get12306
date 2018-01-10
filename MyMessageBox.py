# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QMessageBox
#
# from UserPage import Ui_Form
#
#
# class MyWindow(QtWidgets.QWidget,Ui_Form):
#     def __init__(self):
#         super(MyWindow, self).__init__()
#         self.myButton = QtWidgets.QPushButton(self)
#         self.myButton.setObjectName("myButton")
#         # self.myButton.setText(text)
#         self.myButton.clicked.connect(self.msg)
#
#     def msg(self,title,message):
#         reply = QMessageBox.information(self,  # 使用infomation信息框
#                                         title,
#                                         message,
#                                         QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     myshow = MyWindow()
#     myshow.show()
#     sys.exit(app.exec_())