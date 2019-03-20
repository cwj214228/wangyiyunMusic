# -*- coding: utf-8 -*-
import scrapy
import json

from wangyiyunMusic.items import WangyiyunmusicItem


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['musicapi.leanapp.cn']
    start_urls = ['http://musicapi.leanapp.cn/comment/music']

    def parse(self, response):
        for offset in range(0,1000):
            id = '1313354324'
            limit = '20'
            offset = offset+1
            url = 'http://musicapi.leanapp.cn/comment/music?' + 'id=' + id + '&limit=' + limit + '&offset=' + str(
                offset)
            yield scrapy.Request(url, callback=self.parse_getMseeage)

    def parse_getMseeage(self,response):
        text=response.body
        jsondata = json.loads(text.decode('utf-8'))
        # print(jsondata)
        All_comments = jsondata['comments']
        item=WangyiyunmusicItem()
        for All_comment in All_comments:
            # 用户名
            item['nickname'] = All_comment['user']['nickname'].replace(',', '，')
            # 用户ID
            item['userId'] = str(All_comment['user']['userId'])
            # 评论内容
            item['content'] = All_comment['content'].strip().replace('\n', '').replace(',', '，')
            yield item

