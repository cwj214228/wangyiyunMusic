# -*- coding: utf-8 -*-
import xlsxwriter
import time
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WangyiyunmusicPipeline(object):
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.f = open("D:/爬虫数据/"+str(item['name'])+'.txt', 'a')
        try:
            line = item['content'] + '\n'
            self.f.write(line)
        except:
            pass
        return item


    def close_spider(self, spider):
        self.f.close()
        pass
