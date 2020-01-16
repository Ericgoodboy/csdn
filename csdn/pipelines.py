# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy.exporters import JsonLinesItemExporter
from scrapy import Spider
logger = logging.getLogger(__name__)

class CsdnPipeline(object):
    def __init__(self):
        self.fp = open("data.json","wb")
        self.expoter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
        self.count = 1
        pass

    def process_item(self, item, spider:Spider):
        logging.debug(">"*30)
        self.count+=1
        self.expoter.export_item(item)

        # logging.debug(item)
        if self.count>100:
            spider.close(spider,"enough")
        # print(">"*30)
        # print(self.count)
        # print("="*30)
    def __del__(self):
        self.fp.close()