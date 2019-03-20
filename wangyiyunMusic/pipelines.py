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
        self.workbook = xlsxwriter.Workbook('D:/爬虫数据/'+time.strftime("wangyiyun")+'.xlsx')  # 创建一个Excel文件
        self.worksheet = self.workbook.add_worksheet()  # 创建一个sheet
        self.num0=0

    def process_item(self, item, spider):
        self.num0 = self.num0 + 1
        row = 'A' + str(self.num0)
        data = [item['nickname'], item['userId'], item['content']]
        self.worksheet.write_row(row, data)
        return item

    def close_spider(self, spider):
        self.workbook.close()
