# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup  #从网页抓取数据
import urllib2,urllib

x=0
for i in range(1,11):   #下载前十页

    url = 'https://www.dbmeinv.com/?pager_offset={}'.format(str(i))
    def crawl(url): #模拟浏览器，加上heaers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        req = urllib2.Request(url,headers=headers) #用地址创建一个request对象
        page = urllib2.urlopen(req,timeout=20)   #打开网页
        contents = page.read()  #获取源码
        #print contents

        soup = BeautifulSoup(contents,'html.parser')
        my_girl = soup.find_all('img')
        for girl in my_girl:
            link = girl.get('src')
            #print link
            global x
            urllib.urlretrieve(link,'image\%s.jpg' %x) #下载
            x+=1

    crawl(url)
