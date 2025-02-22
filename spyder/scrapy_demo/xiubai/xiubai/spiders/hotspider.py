# -*- coding: utf-8 -*-
import scrapy
from xiubai.items import XiubaiItem

class HotspiderSpider(scrapy.Spider):
    name = 'hotspider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/8hr/page/2/']

    def parse(self, response):
        item = XiubaiItem()

        # 找到热门段子主体
        main = response.xpath('//div[@id="content-left"]/div')

        for div in main:
            # 段子作者
            item['author'] = div.xpath('.//h2/text()').extract()[0]
            # 段子主体
            item['body'] = ''.join(div.xpath('a[@class="contentHerf"]/div/span[1]/text()').extract())
            # 段子 footer
            item['funNum'] = div.xpath('.//span[@class="stats-vote"]/i/text()').extract()[0]
            # 段子 comNum
            item['comNum'] = div.xpath('.//span[@class="stats-comments"]/a/i/text()').extract()[0]
            yield item

