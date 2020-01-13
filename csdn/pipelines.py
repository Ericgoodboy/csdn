# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
logger = logging.getLogger(__name__)

class CsdnPipeline(object):
    def process_item(self, item, spider):
        logging.debug(">"*30)
        logging.debug(item)
        pass
