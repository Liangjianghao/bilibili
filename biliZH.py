#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/30 16:36
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import json
import time
import datetime
import pymysql
import re
from lxml import html

tableName='biliTable'

# CREATE TABLE `biliTable` (
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
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='b站总表';

connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='bili',
    charset='utf8mb4'
)
cursor = connect.cursor()
def analyVideo(videoUrl):
    pattern = re.compile('(?<=av).*')
    aid = pattern.findall(videoUrl)[0]
    timeStam = int(time.time())
    getinforUrl = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % aid
    # print(getinforUrl)
    response = requests.get(getinforUrl, verify=False).content
    requests.adapters.DEFAULT_RETRIES = 5
    jsondata = json.loads(response)
    # print(jsondata)
    video = jsondata['data']
    videoUrl = url
    pubdate = video['pubdate']
    uploadTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pubdate)))
    userName = video['owner']['name']
    videoCover = video['pic']
    videoTitle = video['title']
    if "'" in videoTitle:
        videoTitle = videoTitle.replace("'", "\\'")
    playNum = video['stat']['view']
    danmuNum = video['stat']['danmaku']
    contenNum = video['stat']['reply']
    saveNum = video['stat']['favorite']
    coinNum = video['stat']['coin']
    likeNum = video['stat']['like']
    dislikeNum = video['stat']['dislike']
    shareNum = video['stat']['share']
    danmuID = video['cid']
    danmu1=0
    danmu2=0
    danmu3=0
    sql = "REPLACE INTO %s (videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s')" % (tableName,videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)
    # print(sql)
    cursor.execute(sql)
    connect.commit()

for x in range(9000000,10000000):
    print('正在采集第%s个视频'%str(x))
    url='https://www.bilibili.com/video/av%s'%x
    try:
        analyVideo(url)
    except Exception as e:
        print('报错：%s'%e)
        continue
