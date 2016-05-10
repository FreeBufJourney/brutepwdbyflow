#-*-coding=UTF-8
import json
import pdb


class PostDataWrapper():

    def __init__(self,postdata,decode_postdata):
        self.username_list = ['username','email','account','u','userid']
        self.password_list = ['password','p','passwd']
        self.maindata,self.extradata = self.__get_maindata(postdata,decode_postdata)


    def __get_maindata(self,postdata,decode_postdata):
        postdatadict = {}
        postdatalist = postdata.split('&')
        maindata = {}
        extrdata = {}
        for item in postdatalist:
            name,value = str(item.split('=')[0]),str(item.split('=')[1])
            postdatadict[name] = value
        #从网页中解析出来了username和passowrd
        if decode_postdata:
            username = decode_postdata['username']
            password = decode_postdata['password']
            captcha = decode_postdata['captcha']
            if captcha != '':
                if captcha in postdatadict:
                    maindata['captcha'] = captcha
                    del postdatadict[captcha]
            if username in postdatadict:
                maindata['username'] = username
                del postdatadict[username]
            if password in postdatadict:
                maindata['password'] = password
                del postdatadict[password]
            return maindata,postdatadict
        else:
            for username in self.username_list:
                print(username)
                if username in postdatadict:
                    maindata['username'] = username
                    del postdatadict[username]
                    break
                if username.upper() in postdatadict:
                    maindata['username'] = username.upper()
                    del postdatadict[username.upper()]
                    break
            for password in self.password_list:
                print(password)
                if password in postdatadict:
                    maindata['password'] = password
                    del postdatadict[password]
                    break
                if password.upper() in postdatadict:
                    maindata['password'] = password.upper()
                    del postdatadict[password.upper()]
                    break
            return maindata,postdatadict




class DataWrapper():

    def __init__(self,data,decodeData):
        self.header = {}
        self.hasCaptcha = False
        self.captcha_url = ''
        self.postdata = None
        self.url = ''
        self.decode_post_data = decodeData
        self.__decode_data(data)

    def __decode_data(self,data):
        my_postdata = data.split('\n\n')[1]
        my_header = data.split('\r\n\r\n')[0]
        self.postdata = PostDataWrapper(my_postdata,self.decode_post_data)
        self.posturl= self.__decode_all_header(my_header)



    def __decode_all_header(self,my_header):
        '''
        :param my_header:
        :return:
        '''
        headers = my_header.split('\n')
        first_line = headers[0]
        post_url_postfix_index = first_line.rfind(' ')
        post_url_prefix_index = first_line.find(' ') +1
        self.__decode_header(my_header)
        post_url = first_line[post_url_prefix_index:post_url_postfix_index]
        post_url = self.__decode_post_url(post_url)
        return post_url

    def __decode_header(self,my_header):
        index = my_header.find('\n')
        header = my_header[index+1:]
        header_datas = header.split('\n')
        header_dict = {}
        for item in header_datas:
            index= item.find(':')
            header_name,header_value = str(item[:index]),str(item[index+1:])
            header_dict[header_name] = header_value
        self.header['host'] = header_dict['Host']
        self.header['User-Agent'] = header_dict['User-Agent']
        self.header['Referer'] = header_dict['Referer']
        self.header['Connection'] = header_dict['Connection']


    def __decode_post_url(self,post_url):
        decoded_post_url = ''
        post_url = post_url.strip()
        if not post_url.startswith('http'):
            if post_url.startswith('/'):
                decoded_post_url = 'http://'+self.header['host']+post_url
            else:
                pass
        else:
            decoded_post_url = post_url
        return  decoded_post_url

if __name__ == '__main__':
    postdata = '_xsrf=43b225731ad57fb6a3b6f52904a760e9&password=12345789&remember_me=true&email=wang_monkey%40163.com'
    decode_data = {}
    postdata = 'username=wyj&password=wyj&rymz=76EQ'
    decode_data = {'captcha': 'rymz', 'password': 'password', 'username': 'username'}
    data = PostDataWrapper(postdata,decode_data)
    print(str(data.maindata))