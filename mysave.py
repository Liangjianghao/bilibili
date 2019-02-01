#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/27 11:52
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from selenium import webdriver
import time


UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
# headers = {"User-Agent": UA, "Referer": "https://space.bilibili.com/33388057/,'Connection': 'keep-alive'"}
headers = {'User-Agent': UA,
           'Connection': 'keep-alive'
           }
driver = webdriver.Chrome()
url = "https://www.bilibili.com/"
driver.get(url)
time.sleep(25)

# cookie_dict={}
#
# # 获取cookie列表
# cookie_list = driver.get_cookies()
# # 格式化打印cookie
# for cookie in cookie_list:
#     cookie_dict[cookie['name']] = cookie['value']
# print(cookie_dict)
#
# cookie_list = driver.get_cookies()
# # 格式化打印cookie
# for cookie in cookie_list:
#     cookie_dict[cookie['name']] = cookie['value']
# print(cookie_dict)

csrf = input("input:")
print(csrf)

cookie =[item["name"] + ":" + item["value"] for item in driver.get_cookies()]
cookiestr = ';'.join(item for item in cookie)
cook_map = {}
for item in cookie :
    thisStr = item.split(':')
    cook_map[thisStr[0]] = thisStr[1]
# print (cook_map)
cookies = requests.utils.cookiejar_from_dict(cook_map, cookiejar=None, overwrite=True)
session = requests.session()
session.cookies = cookies

with open('saveUrl.txt',encoding='utf-8') as file:
    data=file.readlines()
print(len(data))

failedNumber=0
for index,video in enumerate(data):
    if index<=1000:
        continue
    try:
        aid=video.split('----')[0].split('av')[1]
        title=video.split('----')[1]
        # print(aid)
        # print(title)
        print('正在收藏第%s条视频：%s'%(str(index+1),title))
        url = 'https://api.bilibili.com/x/v2/fav/video/add'
        data = {
            'aid': aid,
            'fid': '2434435',
            'jsonp': 'jsonp',
            'csrf': csrf
        }
        # print(data)
        response = session.post(url, headers=headers, data=data, verify=False).content
        requests.adapters.DEFAULT_RETRIES = 5
        jsondata = json.loads(response)
        # print(jsondata)
        code = jsondata['code']
        if code==0:
            print('收藏成功')
        elif code<0:
            print('收藏失败：%s'%jsondata)
            break
    except Exception as e:
        print('解析链接:%s报错：%s'%(video,e))
        time.sleep(10)
        failedNumber+=1
    time.sleep(2)
print('共失败%s'%str(failedNumber))

# with open('saveUrl.txt',encoding='utf-8') as file:
#     data=file.readlines()
# print(len(data))
#
#
# for index,video in enumerate(data):
#     UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
#     headers = {"User-Agent": UA, "Referer": "https://space.bilibili.com/35139959/"}
#
#     print('正在解析第%s条数据'%str(index+1))
#     url='https://api.bilibili.com/x/v2/fav/video/add'
#     data={
#         'aid':'32815479',
#         'fid':'615598',
#         'jsonp':'jsonp',
#         'csrf':'8aae96810234889de67604f592698fa6'
#
#     }
#     # session = requests.session()
#     response=requests.session.post(url,headers=headers,data=cookie_dict,verify=False).content
#     requests.adapters.DEFAULT_RETRIES = 5
#     jsondata = json.loads(response)
#     print(jsondata)
#     code=jsondata['code']
#     # print(len(videoArr))
#     # if len(videoArr)==0:
#     #     break
#     # for video in videoArr:
#     #     # print(video['aid'])
#     #     url='https://www.bilibili.com/video/av%s'%video['aid']
#     #     title=video['title']
#     break