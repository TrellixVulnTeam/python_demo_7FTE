# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys


class Downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []
        self.urls = []
        self.nums = ()

    def get_download_url(self):
        req = requests.get(self.target)
        html = req.text
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(target)
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    dl = Downloader()
    dl.get_download_url()
    print('<<一年永恒>>开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '一年永恒.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write(' downloaded: %.3f%' % float(i / dl.nums) + '\r')
        sys.stdout.flush()
    print('《一年永恒》下载完成')
