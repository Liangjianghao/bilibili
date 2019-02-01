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
import pymysql
with open('url.txt') as f:
    data=f.readlines()
print('共解析%s条网址'%len(data))

# CREATE TABLE `biliTest` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `videoTitle` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `videoUrl` varchar(255) DEFAULT NULL COMMENT '视频地址',
#   `videoCover` varchar(255) DEFAULT NULL COMMENT '封面地址',
#   `userName` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `uploadTime` datetime DEFAULT NULL COMMENT'视频上传时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `danmuNum` int(11) DEFAULT NULL COMMENT '弹幕数',
#   `contenNum` int(11) DEFAULT NULL COMMENT '评论数',
#   `saveNum` int(11) DEFAULT NULL COMMENT '收藏数',
#   `coinNum` int(11) DEFAULT NULL COMMENT '硬币数',
#   `likeNum` int(11) DEFAULT NULL COMMENT '喜欢数',
#   `dislikeNum` int(11) DEFAULT NULL COMMENT '不喜欢数',
#   `shareNum` int(11) DEFAULT NULL COMMENT '分享数',
#   `danmuID` int(11) DEFAULT NULL COMMENT '弹幕id',
#   `danmu1` int(11) DEFAULT NULL COMMENT '相关弹幕一',
#   `danmu2` int(11) DEFAULT NULL COMMENT '相关弹幕二',
#   `danmu3` int(11) DEFAULT NULL COMMENT '相关弹幕三',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='b站测试表';

url='https://api.bilibili.com/x/v1/dm/list.so?oid=41671799'#获取弹幕

def insertChatContent(videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3):
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
    sql = "INSERT INTO bilitest (videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s')" % (videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)
    # print(sql)
    insertSql = "INSERT INTO bilitest (videoTitle, videoUrl,videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)SELECT '%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s'  FROM bilitest WHERE NOT EXISTS(SELECT videoUrl FROM bilitest WHERE videoUrl='%s')LIMIT 1" % (videoTitle, videoUrl,videoCover, userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3,videoUrl)
    #print(insertSql)
    cursor.execute(insertSql)
    connect.commit()

for index,url in enumerate(data):
    print('解析第%s条网址:%s'%(index+1,url))
    pattern=re.compile('(?<=av).+?(?=\?)')
    aid=pattern.findall(url)[0]
    timeStam=int(time.time())
    getCidUrl='https://api.bilibili.com/x/web-interface/archive/related?aid=%s&ampcallback=jqueryCallback_bili_6&ampjsonp=jsonp&amp_=%s'%(aid,timeStam)
    print(getCidUrl)
    # break
    response=requests.get(getCidUrl,verify=False).content
    requests.adapters.DEFAULT_RETRIES = 5
    jsondata=json.loads(response)
    # print(jsondata)
    videoArr=jsondata['data']
    print(len(videoArr))
    for video in videoArr:
        try:
        # print(video['aid'])
            videoUrl='https://www.bilibili.com/video/av%s'%str(video['aid'])
            pubdate = video['pubdate']
            uploadTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pubdate)))
            userName = video['owner']['name']
            videoCover=video['pic']
            videoTitle = video['title']
            if "'" in videoTitle:
                videoTitle=videoTitle.replace("'","\\'")
            playNum = video['stat']['view']
            danmuNum = video['stat']['danmaku']
            contenNum = video['stat']['reply']
            saveNum = video['stat']['favorite']
            coinNum = video['stat']['coin']
            likeNum = video['stat']['like']
            dislikeNum = video['stat']['dislike']
            shareNum = video['stat']['share']
            danmuID=video['cid']
            danmu1=0
            danmu2=0
            danmu3=0
            print('正在处理第%s条数据：%s' % (str(index + 1), videoTitle))
            insertChatContent(videoTitle, videoUrl,videoCover, userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)
        except Exception as e:
            print(e)
            continue
    # break