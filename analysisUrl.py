#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/2 18:47
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import sys
import requests
from lxml import html
import json
import time
import bs4
from selenium import webdriver
import re
import json
with open('url.txt') as f:
    data=f.readlines()
print('共解析%s条网址'%len(data))

# url='https://api.bilibili.com/x/web-interface/archive/related?aid=11632419&ampcallback=jqueryCallback_bili_6&ampjsonp=jsonp&amp_=1533211227760'
# # url='https://api.bilibili.com/x/web-interface/archive/related?aid=11632419&callback=jqueryCallback_bili_6&jsonp=jsonp&_=1533211227760'
#
# response = requests.get(url,verify=False).content
# # requests.adapters.DEFAULT_RETRIES = 5
# # print(response)
# jsondata = json.loads(response)
# # print(jsondata['data'])
# videoArr=jsondata['data']
# print(len(videoArr))
# time.sleep(1)
for index,url in enumerate(data):
    print('解析第%s条网址:%s'%(index+1,url))
    # getBaseInfoUrl='https://api.bilibili.com/x/web-interface/archive/stat?aid=%s'%aid
    # getSimilarUrl='https://api.bilibili.com/x/web-interface/archive/related?aid=14582526&callback=jqueryCallback_bili_6&jsonp=jsonp&_=1533207727829'
    pattern=re.compile('(?<=av).+?(?=\?)')
    aid=pattern.findall(url)[0]
    timeStam=int(time.time())
    # print(timeStam)
    getCidUrl='https://api.bilibili.com/x/web-interface/archive/related?aid=%s&ampcallback=jqueryCallback_bili_6&ampjsonp=jsonp&amp_=%s'%(aid,timeStam)
    print(getCidUrl)
    # driver=webdriver.Chrome()
    # driver.get(getCidUrl)
    response=requests.get(getCidUrl,verify=False).content
    requests.adapters.DEFAULT_RETRIES = 5
    # print(response['code'])
    jsondata=json.loads(response)
    # print(jsondata['code'])
    print(jsondata)
    # newUrl=getCidUrl.replace('&','&amp')
    # print(newUrl)
    # time.sleep(3)
    # response=requests.get(newUrl)
    # print(response)
    # time.sleep(2)
    # driver.get(newUrl)


    # print(getCidUrl)
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    #
    # response=requests.get(getCidUrl,headers=headers).content
    # time.sleep(2)
    # print(response)
    # time.sleep(1000)
    # testUrl='https://api.bilibili.com/x/web-interface/archive/related?aid=11632419&amp;amp;callback=jqueryCallback_bili_6&amp;amp;jsonp=jsonp&amp;amp;_=1533211227760'
    # 1='https://api.bilibili.com/x/web-interface/archive/related?aid=11632419&amp;amp;callback=jqueryCallback_bili_6&amp;amp;jsonp=jsonp&amp;amp;_=1533211227760'
    # 2='https://api.bilibili.com/x/web-interface/archive/related?aid=11632419&amp;callback=jqueryCallback_bili_6&amp;jsonp=jsonp&amp;_=1533211227760'
    break