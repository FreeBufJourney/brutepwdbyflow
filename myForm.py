#-*-coding=UTF-8 -*_
import os
import pdb
# from PyQt4 import QtGui,QtCore,QtNetwork
from PyQt4 import QtGui,QtCore,QtNetwork
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidgetItem
from MyWidgets.PostDataHelper import DataWrapper
from MyWidgets.SimulateHelper import MyLoginThread
from MyWidgets.formHelper import form_url
from multiprocessing import freeze_support
freeze_support()
from MyWidgets.proxyHelper import MyProxy, MyProxy2
# from ui import Ui_MainWindow
# from ui2 import Ui_MainWindow
# from task6 import Ui_MainWindow
from task6ui import Ui_MainWindow

class MyForm(Ui_MainWindow):
    
    def __init__(self):
        super(MyForm, self).__init__()
        self.my_proxy = MyProxy()
        self.my_proxy.start()
        self.my_updateUI_proxy = MyProxy2()
        self.my_updateUI_proxy.updatedUI.connect(self.show_postdata)
        self.my_updateUI_proxy.start()
        self.url = ''
        self.main_postdata = {}
        self.all_url = []
        self.processing_num = 0
        # self.username_file = 'c:/username.txtx'
        # self.pwd_file_path = 'c:/password.txt'


    #for task6
    # def setupUi(self, MainWindow):
    #     super().setupUi(MainWindow)
    #     self.tableWidget.setSortingEnabled(True)
    #     self.charFormat = self.postdata_textEdit.textCursor().charFormat()
    #     self.username_file = 'D:/username.txt'
    #     self.pwd_file = 'D:/password.txt'
    #     self.statusbar.showMessage('进度')
    #     self.usrname_file_path_label.setText('用户名文件:'+self.username_file)
    #     self.pwd_file_path_label.setText('密码文件:'+self.pwd_file)
    #     networkmanager = self.webView.page().networkAccessManager()
    #     proxy = QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.HttpProxy,'127.0.0.1',8899)
    #     networkmanager.setProxy(proxy)
    #     self.webView.page().setNetworkAccessManager(networkmanager)
    #     self.charFormat = self.postdata_textEdit.textCursor().charFormat()
    #     self.webView.loadProgress[int].connect(self.loading)
    #
    #     self.showUrl_btn.clicked.connect(self.show_webpage)
    #     self.username_mark_btn.clicked.connect(self.mark_user)
    #     self.pwd_mark_btn.clicked.connect(self.mark_pwd)
    #     self.remove_mark_btn.clicked.connect(self.remove_marks)
    #     self.save_mark_btn.clicked.connect(self.save_url)
    #     self.Urls_listWidget.itemDoubleClicked.connect(self.deleteItem)
    #
    #     self.UserName_file_btn.clicked.connect(self.open_username_file)
    #     self.pwd_file_btn.clicked.connect(self.open_pwd_file)
    #     self.start_btn.clicked.connect(self.start_login)
    #     self.save_result_btn.clicked.connect(self.save_result)

    # for task6ui
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.tableWidget.setSortingEnabled(True)
        self.username_file = 'D:/username.txt'
        self.pwd_file = 'D:/password.txt'
        self.statusbar.showMessage('进度')
        self.usrname_file_path_label.setText('用户名文件:'+self.username_file)
        self.pwd_file_path_label.setText('密码文件:'+self.pwd_file)
        networkmanager = self.webView.page().networkAccessManager()
        proxy = QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.HttpProxy,'127.0.0.1',8899)
        networkmanager.setProxy(proxy)
        self.webView.page().setNetworkAccessManager(networkmanager)
        self.webView.loadProgress[int].connect(self.loading)

        self.showUrl_btn.clicked.connect(self.show_webpage)
        self.Urls_listWidget.itemDoubleClicked.connect(self.deleteItem)

        self.UserName_file_btn.clicked.connect(self.open_username_file)
        self.pwd_file_btn.clicked.connect(self.open_pwd_file)
        self.start_btn.clicked.connect(self.start_login)
        self.save_result_btn.clicked.connect(self.save_result)

    def loading(self,percent):
        self.process_label.setText('Loading %d%%' %percent)

    def show_webpage(self):
        url = self.Url_lineEdit.text().strip()
        self.webView.load(QtCore.QUrl(url))
        try:
            decodehtml = form_url(url)
            self.main_postdata = decodehtml.maindata
            print(self.main_postdata)
            self.decode_html = decodehtml
        except Exception as e:
            print(e)
            self.main_postdata = {}
            self.decode_html = None

    def show_postdata(self,data):
        password = ''
        username = ''
        if  self.main_postdata:
            password = self.main_postdata['password']
            username = self.main_postdata['username']
            print('username=%s,pwd=%s'%(username,password))
        if data.strip() != '':
            self.postdata = data
            self.datawrapper = DataWrapper(data,self.main_postdata)
            self.datawrapper.url = self.Url_lineEdit.text().strip()
            if self.decode_html:
                self.datawrapper.hasCaptcha = self.decode_html.hasCaptcha
                self.datawrapper.captcha_url = self.decode_html.captcha_url
            else:
                self.datawrapper.hasCaptcha = False
                self.datawrapper.captcha_url = ''

            print('maindata',self.datawrapper.postdata.maindata)
            print('extradata',self.datawrapper.postdata.extradata)

            #保存结果
            self.save_url()

    def mark_user(self):
        textCursor2 = self.postdata_textEdit.textCursor()
        print(textCursor2.selectedText())
        self.datawrapper.postdata.maindata['username'] = textCursor2.selectedText()
        keyword = textCursor2.charFormat()
        keyword.setForeground(QtGui.QBrush(Qt.blue))
        keyword.setFontWeight(QtGui.QFont.Bold)
        textCursor2.setCharFormat(keyword)
        # textCursor2.setPosition(end,QtGui.QTextCursor.KeepAnchor)
        self.postdata_textEdit.setTextCursor(textCursor2)

    def mark_pwd(self):

        textCursor2 = self.postdata_textEdit.textCursor()
        print(textCursor2.selectedText())
        self.datawrapper.postdata.maindata['password'] = textCursor2.selectedText()
        keyword = textCursor2.charFormat()
        keyword.setForeground(QtGui.QBrush(Qt.blue))
        keyword.setFontWeight(QtGui.QFont.Bold)
        textCursor2.setCharFormat(keyword)
        # textCursor2.setPosition(end,QtGui.QTextCursor.KeepAnchor)
        self.postdata_textEdit.setTextCursor(textCursor2)

    def remove_marks(self):
        self.postdata_textEdit.setPlainText('')
        self.postdata_textEdit.clear()
        textCursor = self.postdata_textEdit.textCursor()
        textCursor.setCharFormat(self.charFormat)
        self.postdata_textEdit.setTextCursor(textCursor)
        self.postdata_textEdit.setPlainText(self.postdata)



    def save_url(self):
        all_website_urls = [data.url for data in self.all_url]
        print(all_website_urls)
        if self.datawrapper.url not in all_website_urls:
            self.all_url.append(self.datawrapper)
            item = QtGui.QListWidgetItem(self.datawrapper.posturl)
            self.Urls_listWidget.addItem(item)

    def deleteItem(self):
        selected_item = self.Urls_listWidget.selectedItems()[0]
        selected_post_url = selected_item.text()
        #从列表中删除
        for website_data in self.all_url:
            if selected_post_url == website_data.posturl:
                self.all_url.remove(website_data)
        selected_item_index = self.Urls_listWidget.indexFromItem(selected_item).row()
        model = self.Urls_listWidget.model()
        model.removeRow(selected_item_index)

    def open_username_file(self):
        name_file = QtGui.QFileDialog.getOpenFileName(None,'用户名文件','C:/')
        if name_file:
            self.username_file = name_file
            self.usrname_file_path_label.setText('用户名文件:'+self.username_file)

    def open_pwd_file(self):
        name_file = QtGui.QFileDialog.getOpenFileName(None,'密码文件','C:/')
        if name_file:
            self.pwd_file = name_file
            self.pwd_file_path_label.setText('密码文件:'+self.pwd_file)


    def start_login(self):
        # self.tableWidget.clear()
        # self.tableWidget.setRowCount(0)
        count = len(self.all_url)
        if count == 0:
            return
        self.__read_file()
        self.ThreadList = []
        self.activedthreadleft = len(self.all_url)
        for url in self.all_url:
            print(url.posturl)
            self.loginthread = MyLoginThread(self.username_list,self.pwd_list,url)
            self.loginthread.trigger.connect(self.updateTableWidget)
            self.loginthread.finished.connect(self.threadleft)
            self.loginthread.processing.connect(self.processing_show)
            self.ThreadList.append(self.loginthread)

        for t in self.ThreadList:
            t.start()

    def __read_file(self):
        print(self.username_file)
        usernames = []
        pwds = []
        try:
            with open(self.username_file) as file:
                try:
                    for line in file:
                        usernames.append(line.strip())
                except Exception:
                    QtGui.QMessageBox.warning(None,'错误','读取用户名弱口令文件错误')
                    return
        except Exception:
            QtGui.QMessageBox.warning(None,'错误','读取用户名弱口令文件错误')
            return

        try:
            with open(self.pwd_file) as file:
                try:
                    for line in file:
                        pwds.append(line.strip())
                except:
                    QtGui.QMessageBox.warning(None,'错误','读取密码弱口令文件错误')
                    return
        except Exception:
            QtGui.QMessageBox.warning(None,'错误','读取密码弱口令文件错误')
            return
        self.username_list = usernames
        self.pwd_list = pwds


    def __login(self,url):
        print('----------------%s'%(url.posturl))
        self.loginthread = MyLoginThread(self.username_list,self.pwd_list,url)
        self.loginthread.trigger.connect(self.updateTableWidget)
        self.loginthread.start()
        # pdb.set_trace()

    def updateTableWidget(self,responseinfo):
        rowPostion = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPostion)
        self.tableWidget.setItem(rowPostion,0,QTableWidgetItem(responseinfo.username))
        self.tableWidget.setItem(rowPostion,1,QTableWidgetItem(responseinfo.password))
        self.tableWidget.setItem(rowPostion,2,QTableWidgetItem(responseinfo.url))

    def threadleft(self):
        self.activedthreadleft -= 1
        print(self.activedthreadleft)
        if self.activedthreadleft == 0:
            QtGui.QMessageBox.warning(None,'Messagebox','执行完毕')

    def processing_show(self):
        self.processing_num += 1
        processing_str = str(self.processing_num)
        self.statusbar.showMessage(processing_str)

    def save_result(self):
        selected_directry = QtGui.QFileDialog.getExistingDirectory(None,'select Directory','C:/')
        if selected_directry:
            current_directory = selected_directry
            export_file  =current_directory + '\\'+'result.txt'
            f = open(export_file,'w')
            f.write('用户名'+'       '+'密码'+'     '+'网址'+'\n')
            row_count = self.tableWidget.rowCount()
            for i in range(0,row_count):
                url = self.tableWidget.item(i,2).text()
                usrname = self.tableWidget.item(i,0).text()
                pwd = self.tableWidget.item(i,1).text()
                f.write(usrname+'       '+pwd+'     '+url+'\n')
            f.close()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = MyForm()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
        
        