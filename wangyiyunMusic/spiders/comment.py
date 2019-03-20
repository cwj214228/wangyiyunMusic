# -*- coding: utf-8 -*-
import scrapy
import json
import random

from wangyiyunMusic.items import WangyiyunmusicItem, musiclistItem


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['musicapi.leanapp.cn']
    start_urls = ['http://musicapi.leanapp.cn/top/list?idx=1']

    def parse(self, response):
        # 解析json数据，获得所有热歌的id
        text = response.body
        jsondata = json.loads(text.decode('utf-8'))
        musiclist = jsondata['playlist']['tracks']
        musicItem=musiclistItem()
        # 自制ip连接池，把有用的ip和它对应的端口放在队列中，一会方便随机调用
        IPPOOL = [
            {"ipaddr": "139.196.90.80:80"},
            {"ipaddr": "117.191.11.107:80"},
            {"ipaddr": "59.49.72.138:80"}
        ]
        # 根据歌曲的id，爬取评论，每首歌爬取10页评论
        for music in musiclist:
            musicItem['id'] = music['id']
            thisip = random.choice(IPPOOL)
            # print(thisip)
            for offset in range(0,10):
                limit = '20'
                offset = offset + 1
                url = 'http://musicapi.leanapp.cn/comment/music?' + \
                      'id=' + str(musicItem['id']) + '&limit=' + limit + '&offset=' + str(offset)+\
                '&proxy=http://'+thisip['ipaddr']+'/proxy.pac'

                yield scrapy.Request(url, callback=self.parse_getComment)

    # 这个方法用于解析评论的json数据，把解析好的数据打包发给pipeline。py进一步处理
    def parse_getComment(self,response):
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

