# -*- coding:utf-8 -*-
import requests
import logging
from bs4 import BeautifulSoup
__author__ = 'JackGao'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

tag_list = ['日本', '台湾', '欧美', '美国', '英国', '香港', '华语', '内地', '中国', 'UK', '韩国', '粤语', '法国', '英伦', '德国',
            '大陆', '港台', '爱尔兰', '瑞典', 'US', '国语', 'Japan', '新加坡', 'HK', '华语音乐', '冰岛', '挪威', '日本音乐', '台灣'
            '意大利', '西班牙', '马来西亚', '俄罗斯', '法语', '欧美音乐', '北欧']

base_url = 'https://music.douban.com/tag/%s?start=%d&type=R'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}


def open_url(tag, page, cookie=''):
    cur_url = base_url % (tag_list[tag], page*20)
    temp_header = header.copy()
    # 判断 cookie 是否为空
    if cookie:
        temp_header['Cookie'] = cookie

    r = requests.get(cur_url, headers=temp_header)
    return r


def parse_content(content):
    b = BeautifulSoup(content, "lxml")
    b = b.select('#subject_list .pl2')
    result = []
    for item in b:
        song_name = item.a.string
        strings = item.p.string.split('/')
        singer_name = strings[0]
        pub_date = strings[1]
        rate = item.find_all('span', class_='rating_nums')[0].get_text()
        row = (song_name, singer_name, pub_date, rate)
        result.append(row)
    return result


r = open_url(0, 0)
if r.status_code == 200:
    list1 = parse_content(r.text)
print(list1)


