# coding=utf-8

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes" # 用来标识爬虫，该名字在一个项目必须是唯一的
    def start_requests(self):
        '''
        必须返回一个可迭代的列表（可以是列表，也可以是生成器），
        Scrapy会从这些请求开始抓去网页
        :return:
        '''
        urls=[
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        用于从网页文本中抓取相应内容，我们需要根据自己的需要重写该方法
        :param response:
        :return:
        '''
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)