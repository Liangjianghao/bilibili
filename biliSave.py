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

f=open('saveUrl.txt','a+',encoding='utf-8')
pageNum=1
videoNumber=30
while 1:
    UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
    headers = {"User-Agent": UA, "Referer": "https://space.bilibili.com/35139959/"}
    # url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=447754&tid=0&keyword=&pn=2&order=fav_time&jsonp=jsonp&callback=__jp9'
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=446056&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp26'%pageNum #腿控福利
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=447140&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp32'%pageNum #热舞女神
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=447754&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp40'%pageNum #模特写真
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=445908&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp42'%pageNum #cos福利
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=447667&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp44'%pageNum #二次元福利
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=449095&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp46'%pageNum #游戏福利
    url='https://api.bilibili.com/x/space/fav/arc?vmid=35139959&ps=30&fid=1659932&tid=0&keyword=&pn=%s&order=fav_time&jsonp=jsonp&callback=__jp48'%pageNum #混合福利
    print('正在抓取第%s页收藏'%pageNum)
    # print(url)
    response=requests.get(url,headers=headers,verify=False).content
    requests.adapters.DEFAULT_RETRIES = 5
    # videoData=response.decode("utf-8").split('__jp9(')[1][:-1]
    videoData=response.decode("utf-8")[7:-1]
    # print(videoData)
    jsondata = json.loads(videoData)
    videoArr=jsondata['data']['archives']
    # print(len(videoArr))
    if len(videoArr)==0:
        break
    for video in videoArr:
        # print(video['aid'])
        url='https://www.bilibili.com/video/av%s'%video['aid']
        title=video['title']
        f.write(url+'----'+title+'\n')
    pageNum+=1
f.close()