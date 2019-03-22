# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiyunmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()
    userId = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    pass

class musiclistItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    id = scrapy.Field()
    pass
