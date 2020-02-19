# -*- coding: utf-8 -*-
import scrapy
from csdn.items import CsdnItem
import json

class_name = "ai"
class ClassspiderSpider(scrapy.Spider):
    name = 'classspider'
    allowed_domains = ['blog.csdn.net']
    start_urls = ["https://so.csdn.net/so/search/s.do?p={}&q={}".format(i, class_name) for i in range(1, 100)]
    def parse(self, response):
        index = 1
        for i in response.xpath("//dl/@data-report-click"):
            jsondata=i.get()
            print(index,jsondata)
            obj = json.loads(jsondata)
            index+=1
            if obj["dest"].split("/")[2].split(".")[0]=="blog":
                yield scrapy.Request(obj["dest"], self.parseComent)
    def parseComent(self,response):
        title = response.xpath("//h1[@class='title-article']/text()")[0].get()
        tag = class_name
        body = response.xpath("//div[@id='article_content']")[0].get()
        yield CsdnItem(title=title,tag=tag,body=body)
