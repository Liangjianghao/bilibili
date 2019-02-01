#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/17 17:30
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import re
from selenium import webdriver
import time
import requests
from lxml import html
driver = webdriver.Chrome()
# driver.maximize_window()
f=open('zhaiwu.txt','a+')
for x in range(6499,6800):
    try:
        url='https://www.bilibili.com/v/guochuang/chinese/#/all/default/0/%s/'%x
        url='https://www.bilibili.com/v/dance/otaku/?spm_id_from=333.7.dance_otaku.3#/all/default/0/%s/'%x
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"}
        print('正在爬取第%s页视频：%s' % (str(x),url))
        driver.set_page_load_timeout(20)
        driver.get(url)
    except Exception as e:
        print('报错：%s'%e)
    finally:
        # print(driver.page_source)
        selector=html.fromstring(driver.page_source)
        videoArr=selector.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        print(len(videoArr))
        if len(videoArr)<=0:
            break
        for video in videoArr:
            title=video.xpath('div/div[@class="r"]/a/text()')
            url=video.xpath('div/div[@class="r"]/a/@href')
            if title and title:
                print(title[0]+'：'+url[0][2:])
                f.write(url[0][2:]+'\n')
            else:
                print('无数据')
f.close()