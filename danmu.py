#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/3 22:06
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import pymysql
from lxml import html
url='https://api.bilibili.com/x/v1/dm/list.so?oid=41671799'#获取弹幕
#1w5 条数据 第一次
def select():
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='bili',
        charset='utf8mb4'
    )
    # 获取游标
    cursor = connect.cursor()
    sql = "SELECT * FROM bilitest"
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

def update(videoUrl,danmuNum):
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='bili',
        charset='utf8mb4'
    )
    # 获取游标
    cursor = connect.cursor()
    sql = "UPDATE bilitest SET danmu1='%s' WHERE videoUrl='%s'"%(danmuNum,videoUrl)
    print(sql)
    cursor.execute(sql)
    connect.commit()

urlArr=select()
print('获取到%s条数据'%len(urlArr))
keyWord='可耻的播放量'
def getNumber(hrefs):
    dmNumber=0
    for href in hrefs:
        # print(href)
        if keyWord in href:
            dmNumber+=1
    return  dmNumber
for index,baseurl in enumerate(urlArr):
    try:
        aid=baseurl[14]
        url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=%s'%aid
        print('正在处理第%s条数据：%s'%(str(index+1),baseurl[2]))
        response=requests.get(url).content
        # print(response)
        selector=html.fromstring(response)
        print(selector)
        hrefs=selector.xpath('//d/text()')
        dmNumber=getNumber(hrefs)
        print(dmNumber)
        update(baseurl[2],dmNumber)
    except Exception as e:
        print(e)
        continue
    # break
