#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/28 15:26
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
# url='https://www.bilibili.com/bangumi/play/ep246331'
media_id=''
url='https://bangumi.bilibili.com/review/web_api/media/play?media_id=5839'
url='https://api.bilibili.com/x/web-interface/archive/stat?aid=7429995'#获取视频播放等信息
url='https://api.bilibili.com/x/web-interface/view?aid=7429995'
url='https://api.bilibili.com/x/web-interface/archive/desc?callback=jqueryCallback_bili_2&aid=30373933&page=&jsonp=jsonp&_=1535443759334'#标题
url='https://api.bilibili.com/x/web-interface/view?aid=7429995'#相关信息
url='https://api.bilibili.com/x/v1/dm/list.so?oid=41671799'#获取弹幕
response=requests.get(url).content
print(response)

# 波多野结衣20170505 21:16直播	av10576033
# 这部岛国片，一定要背着家长偷偷看	av12608649
# 女警花首次卧底查案，被流氓鞭打，不料竟失去了第一次	av20652143
# 【TVmosaic】女生私处蜜蜡脱毛全过程！！［马赛克纪录片］	av9576271
# 日本小伙爱上自己的女老师，醉酒后终于得偿所愿！	av24281382
# 真实事件改编，少女被变态大叔囚禁，沦为性奴，看后让人揪心	av25499874
# 牛人制作无翼鸟动画，画风诡异内容令人深思	av19694174
# 日本女高中生直播中忘关摄像头	av6026378
# 【Top 10】十位床上功夫了得的名人，快来认领自己的爱豆吼！@油兔不二字幕组	av8272175
# GTA5 美女诱人的身姿犯规的曲线	av15290781
# 5分钟看完一个老男孩的意淫史	av18130374
# 二哈叫女主起床，女主人还没穿衣服，竟把被子揭开克，女主瞬间爆发	av16410260
# 小仓鼠萌萌萌	av7657291
# 20岁小伙俱乐部解压,遭陌生男子强上,肉体后门被忍痛开启	av27676785
# 雨后小故事  懂得人进	av24782618
# 【真香时刻】女生宿舍比较香？实拍女生宿舍！	av29940377
# 女神钟丽缇-示范四种叫床法	av4231632
# 男友沉迷VR游戏 看女友如何发泄	av8777976
# 【高能】小姐姐碰到了史上最搞笑的医生，真的是皮！	av24682768
#  所有女孩都会做但不会承认的10件事	av6948223