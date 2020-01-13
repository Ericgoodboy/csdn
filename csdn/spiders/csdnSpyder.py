# -*- coding: utf-8 -*-
import scrapy
import logging
from csdn.items import CsdnItem

logger = logging.getLogger(__name__)

class CsdnspyderSpider(scrapy.Spider):
    name = 'csdnSpyder'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://blog.csdn.net/u014427391/article/details/102785219']

    def parse(self, response):
        for i in response.xpath("//div[@class='content']/a/@href"):
            logger.debug(i.get())
            pass
        tags = []
        for i in response.xpath("//a[@class='tag-link']/text()"):
            tag = i.get().strip().lstrip()
            tags.append(tag)
        item = CsdnItem(tags=tags, url=response.url, content=response.xpath("//div[@id='content_views']").get())
        yield item
        