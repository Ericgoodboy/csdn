# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy.exporters import JsonLinesItemExporter
from scrapy import Spider
from bs4 import BeautifulSoup
import jieba
logger = logging.getLogger(__name__)

class CsdnPipeline(object):
    def __init__(self):
        self.fp = open("fulldata2.json","ab")
        self.expoter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
        self.count = 1
        self.stopword = []

        with open("./stopwords_zh.txt", encoding="gbk") as f:
            stopword = [i.strip() for i in f.readlines()]
            stopword += ["\n"] + [""]
        self.stopword = stopword
        print("%"*30)
    def process_item(self, item, spider:Spider):
        logging.debug(">"*30)
        self.count+=1
        soup = BeautifulSoup(item["body"], "lxml")
        cutdata = jieba.cut(soup.text)
        cutdata = [i.strip() for i in cutdata]
        cutdata = [i for i in cutdata if i not in self.stopword]
        item["body"] = cutdata
        self.expoter.export_item(item)


    def __del__(self):
        self.fp.close()