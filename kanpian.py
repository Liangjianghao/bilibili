#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/2 17:57
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

driver=webdriver.Chrome()
f=open('url.txt','a+')
for x in range(1,50):
    print('正在抓取第%s页数据'%x)
    url='https://search.bilibili.com/all?keyword=b站看片&from_source=banner_search&spm_id_from=333.334.banner_link.1&page=%s'%x
    print(url)
    driver.get(url)
    if x==1:
        driver.refresh()
    time.sleep(1)
    page=driver.page_source
    soup = bs4.BeautifulSoup(page, "lxml")
    divs = soup.find_all('li', class_='video matrix')
    print(len(divs))
    for video in divs:
        videoUrl=video.find('a')
        # print(videoUrl.get('href'))
        newUrl=videoUrl['href']
        newUrl=newUrl[2:len(newUrl)]
        print(newUrl)
        f.write(newUrl+'\n')
f.close()