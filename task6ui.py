# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Task6.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1145, 597)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../WIFI_CHEAT.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Url_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.Url_lineEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.Url_lineEdit.setObjectName(_fromUtf8("Url_lineEdit"))
        self.horizontalLayout.addWidget(self.Url_lineEdit)
        self.showUrl_btn = QtGui.QPushButton(self.groupBox)
        self.showUrl_btn.setObjectName(_fromUtf8("showUrl_btn"))
        self.horizontalLayout.addWidget(self.showUrl_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKit.QWebView(self.groupBox)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        self.process_label = QtGui.QLabel(self.groupBox)
        self.process_label.setObjectName(_fromUtf8("process_label"))
        self.verticalLayout.addWidget(self.process_label)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.Urls_listWidget = QtGui.QListWidget(self.groupBox_2)
        self.Urls_listWidget.setObjectName(_fromUtf8("Urls_listWidget"))
        self.verticalLayout_3.addWidget(self.Urls_listWidget)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.UserName_file_btn = QtGui.QPushButton(self.groupBox_4)
        self.UserName_file_btn.setObjectName(_fromUtf8("UserName_file_btn"))
        self.horizontalLayout_3.addWidget(self.UserName_file_btn)
        self.pwd_file_btn = QtGui.QPushButton(self.groupBox_4)
        self.pwd_file_btn.setObjectName(_fromUtf8("pwd_file_btn"))
        self.horizontalLayout_3.addWidget(self.pwd_file_btn)
        self.start_btn = QtGui.QPushButton(self.groupBox_4)
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        self.horizontalLayout_3.addWidget(self.start_btn)
        self.save_result_btn = QtGui.QPushButton(self.groupBox_4)
        self.save_result_btn.setObjectName(_fromUtf8("save_result_btn"))
        self.horizontalLayout_3.addWidget(self.save_result_btn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.groupBox_4)
        self.usrname_file_path_label = QtGui.QLabel(self.centralwidget)
        self.usrname_file_path_label.setObjectName(_fromUtf8("usrname_file_path_label"))
        self.verticalLayout_6.addWidget(self.usrname_file_path_label)
        self.pwd_file_path_label = QtGui.QLabel(self.centralwidget)
        self.pwd_file_path_label.setObjectName(_fromUtf8("usrname_file_path_label"))
        self.verticalLayout_6.addWidget(self.pwd_file_path_label)
        self.pwd_file_path_btn = QtGui.QLabel(self.centralwidget)
        self.pwd_file_path_btn.setObjectName(_fromUtf8("pwd_file_path_btn"))
        self.verticalLayout_6.addWidget(self.pwd_file_path_btn)
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox_5)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1145, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.groupBox.setTitle(_translate("MainWindow", "网页抓包", None))
        self.showUrl_btn.setText(_translate("MainWindow", "开始", None))
        self.process_label.setText(_translate("MainWindow", "进度", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "抓包结果", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "控制台", None))
        self.UserName_file_btn.setText(_translate("MainWindow", "用户名文件", None))
        self.pwd_file_btn.setText(_translate("MainWindow", "密码文件", None))
        self.start_btn.setText(_translate("MainWindow", "开始", None))
        self.save_result_btn.setText(_translate("MainWindow", "保存", None))
        self.usrname_file_path_label.setText(_translate("MainWindow", "用户名文件", None))
        self.pwd_file_path_label.setText(_translate("MainWindow", "密码文件", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "测试结果", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "用户名", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "密码", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "网址", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())