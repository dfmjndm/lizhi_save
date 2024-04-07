import urllib.request
import requests
from urllib.error import URLError, HTTPError, ContentTooShortError
from bs4 import BeautifulSoup
import time
import os
import re

def GetData(url, proxy='', retry =2):
    print('download : ' + url)
    if proxy == '':
        proxy= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'

    request = urllib.request.Request(url)
    request.add_header('User-Agent',proxy)
    try:
        html = urllib.request.urlopen(request).read()
        return html
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('download error :', e.reason)
        if retry>0:                                
            if hasattr(e, 'code') and 500<e.code<600 :
                GetData(url, proxy, retry-1)

def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  
    return filename

# 替换为你自己要爬取的主播的主页地址
url = 'https://www.lizhi.fm/user/36376'

# 创建output目录
if not os.path.exists('./download'):
    os.makedirs('./download')

while url is not None:
    html = GetData(url)
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有音频的链接
    trs = soup.find_all(attrs={'class':'clearfix js-play-data audio-list-item'})
    for tr in trs:
        date_tag = tr.find('p', {'class': 'aduioTime'})
        if date_tag:
            date_str = date_tag.text.strip().split()[0]
            date_str = date_str.replace('-', '/')
            print("The date is: ", date_str)
        link = 'https://cdn5.lizhi.fm/audio/' + date_str + '/' + tr['href'].split('/')[-1] + '_hd.mp3'
        print("The new link is: ", link)
        filename = clean_filename(tr['data-title'])
        music_name = './download/' + filename + '.mp3'
        print("downloads file to ", music_name)
        music_file = requests.get(link).content
        with open(music_name, "wb") as f:
            f.write(music_file)
        time.sleep(2)
    # 翻页
    next_page_tag = soup.find(attrs={'class':'next'})
    if next_page_tag:
        url = 'https://www.lizhi.fm' + next_page_tag['href']
    else:
        break
    print("The next page:", url)
