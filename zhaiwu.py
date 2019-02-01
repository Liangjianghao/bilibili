#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/4 15:02
# @Author : LiangJiangHao
# @Software: PyCharm
import time
import os
import sys
import pymysql
import re
import requests
import json

tableName='bilizhaiwu'


# CREATE TABLE `bilizhaiwu` (
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
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='b站宅舞表';

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


with open('zhaiwu.txt') as f:
    data=f.readlines()
print('共解析%s条网址'%len(data))
for index,url in enumerate(data):
    try:
        print('解析第%s条网址:%s'%(index+1,url))
        pattern=re.compile('(?<=av).+?(?=/)')
        aid=pattern.findall(url)[0]
        timeStam=int(time.time())
        getinforUrl='https://api.bilibili.com/x/web-interface/view?aid=%s'%aid
        # print(getinforUrl)
        response=requests.get(getinforUrl,verify=False).content
        requests.adapters.DEFAULT_RETRIES = 5
        jsondata=json.loads(response)
        # print(jsondata)
        video=jsondata['data']

        videoUrl=url
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
        # insertChatContent(videoTitle, videoUrl,videoCover, userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)
        sql = "INSERT INTO %s (videoTitle, videoUrl, videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s')" % (tableName,videoTitle, videoUrl, videoCover, userName, uploadTime, playNum, danmuNum, contenNum, saveNum, coinNum, likeNum,dislikeNum, shareNum, danmuID, danmu1, danmu2, danmu3)
        insertSql = "INSERT INTO %s (videoTitle, videoUrl,videoCover,userName, uploadTime,playNum, danmuNum, contenNum, saveNum, coinNum,likeNum,dislikeNum,shareNum,danmuID,danmu1,danmu2,danmu3)SELECT '%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s'  FROM %s WHERE NOT EXISTS(SELECT videoUrl FROM %s WHERE videoUrl='%s')LIMIT 1" % (tableName,videoTitle, videoUrl, videoCover, userName, uploadTime, playNum, danmuNum, contenNum, saveNum, coinNum, likeNum,dislikeNum, shareNum, danmuID, danmu1, danmu2, danmu3, tableName,tableName,videoUrl)
        if index == 0:
            cursor.execute(sql)
        else:
            cursor.execute(insertSql)
        connect.commit()
    except Exception as e:
        print(e)
        continue