# -*- coding: utf-8 -*-
import scrapy
from csdn.items import CsdnItem

class CsdnspyderSpider(scrapy.Spider):
    name = 'csdnSpyder'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://blog.csdn.net/u014427391/article/details/102785219']

    def parse(self, response):
        print("="*30)
        print(response.xpath("//div[@id='content_views']").get())
        print(">"*30)
        for i in response.xpath("//div[@class='content']/a/@href"):
            print(i.get())
        print("<"*30)
        print(response.url)
        print("-"*30)
        tags = []
        for i in response.xpath("//a[@class='tag-link']/text()"):
            tag = i.get().strip().lstrip()
            print(tag)
            tags.append(tag)
        print("="*30)
        item = CsdnItem(tags = tags,url = response.url,content=response.xpath("//div[@id='content_views']").get())
        yield item
        