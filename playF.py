#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/29 12:46
# @Author : LiangJiangHao
# @Software: PyCharm
import pymysql
import os
import sys
import time
import datetime
from dateutil import parser


baseTable='bilizhaiwu'
tableName='zhanwuF'
baseTime='2010-1-1'

# CREATE TABLE `zhanwuF` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='b站表';
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='bili',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()

def getinfor(timeStr):
    sql = "SELECT *,sum(playNum) as allnumber FROM %s WHERE uploadtime<='%s' GROUP BY userName ORDER BY allnumber desc limit 20"%(baseTable,timeStr)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)

nowTime = datetime.datetime.now()  # 现在
while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=2)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        video_title = video['videoTitle']
        if "'" in video_title:
            video_title = video_title.replace("'", "\\'")

        video_author = video['userName']
        video_uploadtime = str(video['uploadTime'])[0:10]
        playNum = video['playNum']
        allPlayNum = video['allnumber']
        sql = "insert into %s(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum)
        insertSql = "INSERT INTO %s (video_title,video_author,video_uploadtime,playNum,allPlayNum)SELECT '%s','%s','%s','%s','%s' FROM %s WHERE NOT EXISTS(SELECT video_author FROM %s WHERE video_author='%s' and video_uploadtime='%s')LIMIT 1" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum, tableName,tableName,video_author,datetime_start)
        # print(sql)
        if index==0:
            cursor.execute(sql)
        else:
            cursor.execute(insertSql)
        connect.commit()

