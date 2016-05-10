#encoding: utf-8
from urllib.parse import urlparse
from PyQt4 import QtCore
import logging
from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

class form_url():


    def __init__(self,url):
        self.url = url
        self.init_start()

    def init_start(self):
        # username_list = ['username','u','email','account','phone']
        self.form = self.__get_postform(self.url)
        print(self.form)
        self.maindata = {"username":"","password":"",'captcha':''}
        self.extradata = {}
        self.errortextlength = []
        self.errorHeaders = []
        self.successtextlength = 0
        #解析验证码
        self.hasCaptcha,self.captcha_url = self.__has_captcha()
        #解析form
        self.__decode_form()



    def __get_postform(self,url):
        print(url)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        session = requests.session()
        #为请求添加session
        self.session = session
        response = requests.get(url,headers=headers,timeout=5)
        statusCode = response.status_code
        str_text = response.text
        print(str_text)
        soup = BeautifulSoup(str_text)
        forms = soup.find_all("form")
        form = ""
        #找到提交表单的form
        formCount = len(forms)
        #如果只是存在一个form
        if formCount == 1:
            return forms[0]
        else:
            for x in range(formCount):
                form = forms[x]
                try:
                    flag = False
                    action = form["action"]
                    #如果发现的action中不存在"in"则会直接往下面寻找
                    if action!="":
                        action = action.replace("http://","")
                        index = action.find("/")
                        action = action[index:]
                    if action.find("in")!=-1 or action=="":
                        flag = True
                except:
                    continue
                if flag:
                    break
            return form



    def __decode_form(self):
        # print(str(self.form).encode('gbk', 'ignore').decode('gbk'))
        #得到input标签的数量
        tags_input = self.form.find_all("input")
         #去掉submit
        tags_input = self.__remove_submit_button(tags_input)
        #如果存在验证码，同时去掉验证码标签
        if self.hasCaptcha:
            tag_captcha = self.get_captcha_tag(self.form)
            if tag_captcha:
                tags_input.remove(tag_captcha)
        #找到密码标签
        input_password_index = self.get_password_input(tags_input)
        input_password = tags_input[input_password_index]
        self.maindata["password"] = input_password["name"]
        #找到用户名标签
        input_username = tags_input[input_password_index-1]
        self.maindata["username"] = input_username["name"]
        #去掉用户名和密码标签
        tags_input.remove(input_password)
        tags_input.remove(input_username)
        for tag_input in tags_input:
            #默认第一个为用户名，第二个为密码
            try:
                input_name = tag_input["name"]
            except:
                pass
                continue
            try:
                input_default_value = tag_input["value"]
                self.extradata[input_name] = input_default_value
            except:
                self.extradata[input_name] = ""


    def __remove_submit_button(self,tags_input):
        tags_input = list(tags_input)
        for tag_input in tags_input:
            attributes = tag_input.attrs
            if "type" in attributes:
                typeValue = attributes["type"]
                if(typeValue=="submit"):
                    # del tags_input["type"]
                    tags_input.remove(tag_input)
        return tags_input


    def get_captcha_tag(self,form):
        tag_imgs = form.find_all("img")
        tag_img = tag_imgs[0]
        if not tag_img.find_previous('input'):
            tag_img = tag_imgs[1]
        tag_captcha = tag_img.find_previous("input")
        if tag_captcha:
            input_name = tag_captcha["name"]
            self.maindata["captcha"] = input_name
            return tag_captcha

    def __has_captcha(self):
        img_tag = self.form.find_all("img")
        has_captcha = True
        captcha_url = ''
        #不存在img标签，则不存在验证码
        if len(img_tag) == 0:
            has_captcha = False
        else:
            first_img_tag = img_tag[0]
            if not first_img_tag.find_previous('input'):
                first_img_tag = img_tag[1]
                print(first_img_tag)
            try:
                img_src_value = first_img_tag['src']
                attributes = first_img_tag.attrs
                if 'src' in attributes:
                    src_value = first_img_tag['src']
                    src_url = urlparse(src_value)
                    print(src_value)
                    if 'alt' in attributes:
                        alt_value = first_img_tag['alt']
                        print(alt_value)
                        if alt_value == '验证码' or alt_value == 'captcha':
                            has_captcha = True
                        if alt_value.find('登录')!=-1 or alt_value .find('重置')!=-1:
                            has_captcha = False
                    elif src_url.query:
                        has_captcha = True
                    elif 'onclick' in attributes:
                        has_captcha = True
                    else:
                        has_captcha = False
                if has_captcha:
                    captcha_url = img_src_value
            except:
                has_captcha = False
        if has_captcha:
            urlformat = urlparse(self.url)
            scheme,netloc = urlformat.scheme,urlformat.netloc
            captcha_url = self.__get_captcha_url(captcha_url)
        logger.info(str(has_captcha)+'-----'+captcha_url)
        return has_captcha,captcha_url

    def __get_captcha_url(self,captcha_url):
        #captcha_url不是以http开头
        actionUrl = ''
        if not captcha_url.find("http")==0:
            # #如果action是以"/"开头
            if captcha_url.startswith("/"):
                #获得url中的host
                index = self.url.find("//")
                if index != -1:
                    #协议
                    scheme = self.url[:index+2]
                    url = self.url[index+2:]
                    index =  url.find("/")
                    #获得主机
                    if index != -1:
                        url = url[:index]
                        actionUrl = scheme+url+captcha_url
                    #如果不存在"/"
                    else:
                        actionUrl = scheme+url+"/"+captcha_url
            #如果action不是以"/"开头
            else:
                index = self.url.rfind('/')
                #如果不存在'/'
                if index == -1:
                    actionUrl = self.url+'/'+captcha_url
                #如果'/'在最后
                elif index == len(self.url)-1:
                    actionUrl = self.url+captcha_url
                else:
                    url = self.url[:index+1]
                    actionUrl = url + captcha_url
        #captcha_url是以http开头的
        else:
            actionUrl = captcha_url
        return actionUrl
    #找到密码标签
    def get_password_input(self,tags_input):
        tags_input = list(tags_input)
        i = 0
        for tags_input in tags_input:
            attributes = tags_input.attrs
            if "type" in attributes:
                typeValue = attributes["type"]
                if typeValue == "password":
                   return i
            i = i+1









if __name__ == '__main__':
    url = 'http://www.zhihu.com/#signin'
    url = 'https://account.tophant.com/login.html?response_type=code&client_id=b611bfe4ef417dbc&state=27add119f5c98e6c0ca417080a4a5e95&redirectURL=http://www.freebuf.com'
    url = 'http://www.shanbay.com/accounts/login/'
    # url = 'http://www.v2ex.com/signin'
    url = 'http://news.dbanotes.net/x?fnid=AYeeyAQ2Du'
    url = 'http://www.zhihu.com#signin'
    url = 'http://www.shanbay.com/accounts/login/'
    url = 'http://toutiao.io/ssignin'
    url = 'http://cn.tri.com.tw'
    url = 'http://portal.heptri.hn.sgcc.com.cn/hepcoweb/portletsnew/heptri/login.jsp'
    url = 'http://10.1.17.16:8020/jsp/login.jsp'
    url  = 'http://10.232.208.119/Procheck/login.jsp'
    url  = 'http://newmail.sgcc.com.cn/webmail/login/login.do'
    url = 'http://login.kaixin001.com/'
    form = form_url(url)
    form.init_start()
    print(form.maindata)
    print(form.posturl)