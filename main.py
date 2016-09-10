# -*- coding: utf-8 -*-
# @Date    : 2016/9/9
# @Author  : hrwhisper
import codecs
import re
import os
from datetime import datetime
from multiprocessing.dummy import Pool
import urllib.parse
import requests
from bs4 import BeautifulSoup


def read_file():
    with codecs.open(r'./private', "r", "utf-8") as f:
        res = f.read().split("\n")
        username, password, save_path = res
    return username, password, save_path


class Ucas(object):
    username, password, save_base_path = read_file()  # TODO 文件夹都不存在一路创建

    def __init__(self, processor=4):
        self.__BEAUTIFULSOUPPARSE = 'html5lib'  # or use 'lxml'
        self.session = requests.session()
        self.headers = {
            "Host": "sep.ucas.ac.cn",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        }
        self.course_list = []
        self.to_download = []
        self.max_processor = processor

    def __login_sep(self):
        # 登录sep
        print('Login....')
        url = "http://sep.ucas.ac.cn/slogin"
        post_data = {
            "userName": self.username,
            "pwd": self.password,
            "sb": "sb"
        }
        self.session.post(url, data=post_data, headers=self.headers)

    def get_course_page(self):
        # 从sep中获取Identity Key来登录课程系统，并获取课程信息
        url = "http://sep.ucas.ac.cn/portal/site/16/801"
        r = self.session.get(url, headers=self.headers)
        code = re.findall(r'"http://course.ucas.ac.cn/portal/plogin\?Identity=(.*)"', r.text)[0]

        url = "http://course.ucas.ac.cn/portal/plogin?Identity=" + code
        self.headers['Host'] = "course.ucas.ac.cn"
        html = self.session.get(url, headers=self.headers).text
        url = 'http://course.ucas.ac.cn' + \
              BeautifulSoup(html, self.__BEAUTIFULSOUPPARSE).find('frame', title='mainFrame')['src']
        html = self.session.get(url, headers=self.headers).text
        url = BeautifulSoup(html, self.__BEAUTIFULSOUPPARSE).find('a', class_='icon-sakai-membership')['href']
        html = self.session.get(url, headers=self.headers).text
        url = BeautifulSoup(html, self.__BEAUTIFULSOUPPARSE).find('iframe')['src']
        html = self.session.get(url, headers=self.headers).text
        return html

    def __parse_course_list(self):
        # 获取课程的所有URL
        html = self.get_course_page()
        self.course_list = ['http://course.ucas.ac.cn/portal/site/' + x for x in
                            re.findall(r'http://course.ucas.ac.cn/portal/site/([\S]+)"', html)]

    def __get_all_resource_url(self):
        # 从课程的所有URL中获取对应的所有课件
        print('读取课件中......')
        base_url = 'http://course.ucas.ac.cn/access/content/group/'
        urls = [base_url + x.split('/')[-1] + '/' for x in self.course_list]
        list(map(self.__get_resource_url, urls))
        # for x, y in self.to_download:
        #     print(x, y)

    def __get_resource_url(self, base_url, source_name=None):
        html = self.session.get(base_url, headers=self.headers).text
        res = set()
        urls = BeautifulSoup(html, self.__BEAUTIFULSOUPPARSE).find_all('a')
        if not source_name:
            source_name = BeautifulSoup(html, self.__BEAUTIFULSOUPPARSE).find('h2').text

        for url in urls:
            url = urllib.parse.unquote(url['href'])
            if url == '../': continue
            if url.find('.') == -1:  # directory
                self.__get_resource_url(base_url + url, source_name)
            if url.startswith('http:__'):  # Fix can't download when given a web link. eg: 计算机算法分析与设计
                res.add(self.session.get(base_url + url, headers=self.headers).url)
            else:
                res.add(base_url + url)

        for url in res:
            self.to_download.append((source_name, url))

    def __start_download(self):
        # 多线程下载
        p = Pool(self.max_processor)
        p.map(self.__download_file, self.to_download)
        p.close()
        p.join()

    def __download_file(self, param):
        # 下载文件
        dic_name, url = param

        filename = url.split('/')[-1]
        _path = url[46:].split('/')[1:-1]

        sub_directory = '/'.join(_path) + '/'
        save_path = self.save_base_path + '/' + dic_name + '/' + sub_directory

        r = self.session.get(url, stream=True)
        if not os.path.exists(save_path):  # To create directory
            os.makedirs(save_path)

        save_path += '/' + filename
        if not os.path.exists(save_path):  # To prevent download exists files
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            print('{dic_name}  >> {sub_directory}{filename}   Download success'.format(**locals()))

    def start(self):
        # try:
        self.__login_sep()
        self.__parse_course_list()
        self.__get_all_resource_url()
        self.__start_download()
        # except Exception as e:
        #     print('-----------------', e)


if __name__ == '__main__':
    start = datetime.now()
    s = Ucas()
    s.start()
    print('Task complete, total time:', datetime.now() - start)
