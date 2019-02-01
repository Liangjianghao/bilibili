#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2018/7/22 18:04
# Author  : Bnightning
# Site    : https://www.bnightning.cn
# File    : douyin.py
# Software: PyCharm
# Python Version : 3.6

import requests
from bs4 import BeautifulSoup
import time


def download_file(src, file_path):
    r = requests.get(src, stream=True)
    f = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    return file_path


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

save_path = "H:\\Music\\douyin\\"
url = "https://kuaiyinshi.com/hot/music/?source=dou-yin&page=1"
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
max_page = soup.select('li.page-item > a')[-2].text
for page in range(int(max_page)):
    page_url = "https://kuaiyinshi.com/hot/music/?source=dou-yin&page={}".format(page + 1)
    page_res = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page_res.text, 'lxml')
    lis = soup.select('li.rankbox-item')
    singers = soup.select('div.meta')
    music_names = soup.select('h2.tit > a')
    for i in range(len(lis)):
        music_url = "http:" + lis[i].get('data-audio')
        print("歌名:" + music_names[i].text, singers[i].text, "链接:" + music_url)
        try:
            download_file(music_url,
                          save_path + music_names[i].text + ' - ' + singers[i].text.replace('/', ' ') + ".mp3")
        except:
            pass
    print("第{}页完成~~~".format(page + 1))
    time.sleep(1)