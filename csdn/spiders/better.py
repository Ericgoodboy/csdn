# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.response as Response
from csdn.items import CsdnItem

class BetterSpider(scrapy.Spider):
    name = 'better'
    allowed_domains = ['csdn.net']
    start_urls = ['http://blog.csdn.net/']

    def parse(self, response: Response):
        print(response.url)
        prefix = response.url
        print("*" * 30+"parse")
        return self._explore_all_href(response)
    def _explore_all_href(self,response):
        requests = []
        item_urls = []
        other_urls = []
        mask_user = []
        artical_list = []
        for path in response.xpath("//@href"):
            url = path.get()
            has =False
            for m in mask_user:
                if m in url:
                    has = True
            if has:
                continue
            if "#" in url:
                url = url.split("#")[0]
            if url.startswith("//"):
                pass
            if url.startswith("/") and "nav" in url:
                full_url = "http://blog.csdn.net" + url
                other_urls.append(full_url)
            if "/article/details/" in url:
                item_urls.append(url)
            if url.startswith("https://blog.csdn.net/") and (len(url.split("/")) is 4):
                other_urls.append(url)
                artical_list.append(url+"/article/list/1")
        item_urls = set(item_urls)
        other_urls = set(other_urls)
        for i in item_urls:
            yield scrapy.Request(i,self.format_item)
        for i in other_urls:
            yield scrapy.Request(i,self.parse)
        for i in artical_list:
            yield scrapy.Request(i,self.parse_artical_list)
    def parse_artical_list(self,response:Response):
        list = response.xpath("//div[@class='article-list']//h4/a/@href")
        item_list = []
        for i in list:
            url = i.get()
            if "/article/details/" in url:
                item_list.append(url)
        for i in item_list:
            yield scrapy.Request(i,self.format_item)
        now_url = response.url
        num = now_url.split("/")[-1]
        if len(item_list)>0:
            try:
                num = int(num)+1
                yield scrapy.Request(("/".join(now_url.split("/")[:-1]))+"/"+str(num),self.parse_artical_list)
            except Exception as e:
                pass

    def format_item(self, response:Response):
        title = response.xpath("//h1[@class='title-article']/text()")[0].get()
        body = response.xpath("//div[@id='article_content']")[0].get()
        taga = response.xpath("//a[@class='tag-link']/text()")
        tags = []
        for i in taga:
            tag = i.get()
            tags.append(tag)
        tag = "<spliter>".join(tags)
        yield CsdnItem(title=title, body=body,tag = tag)
        print("*"*30+"parse_item")
        for i in self._explore_all_href(response):
            yield i