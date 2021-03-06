# -*- coding: utf-8 -*-
import scrapy
import json
import random
import pymysql
from wangyiyunMusic.items import WangyiyunmusicItem, musiclistItem


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['musicapi.leanapp.cn']
    start_urls = ['http://musicapi.leanapp.cn/top/list?idx=1']
    conn = pymysql.connect('localhost', 'root', '5201314', 'leecx',
                           charset='utf8')  # 有中文要存入数据库的话要加charset='utf8'
    # 创建游标
    cursor = conn.cursor()

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

        # sql语句
        # 执行插入数据到数据库操作
        sql = "delete from musiclist"
        self.cursor.execute(sql)
        self.conn.commit()
        # 根据歌曲的id，爬取评论，每首歌爬取10页评论
        for music in musiclist:
            musicItem['id'] = music['id']
            musicItem['name'] = music['name']
            thisip = random.choice(IPPOOL)

            self.cursor.execute("insert into musiclist(id,name) values (%s,%s)",
                           (musicItem['id'], musicItem['name']))
            # 提交，不进行提交无法保存到数据库
            self.conn.commit()
            for offset in range(0,100):
                limit = '20'
                offset = offset + 1
                url = 'http://musicapi.leanapp.cn/comment/music?' + \
                      'id=' + str(musicItem['id']) + '&limit=' + limit + '&offset=' + str(offset)+\
                '&proxy=http://'+thisip['ipaddr']+'/proxy.pac'
                yield scrapy.Request(url, callback=self.parse_getComment)

    # 这个方法用于解析评论的json数据，把解析好的数据打包发给pipeline。py进一步处理
    def parse_getComment(self, response):
        text=response.body
        x=response.request.url.split('&')[0]
        musicid=x.split('=')[1]
        sql = "select name from musiclist where id=" +musicid
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        jsondata = json.loads(text.decode('utf-8'))
        All_comments = jsondata['comments']
        item=WangyiyunmusicItem()
        for All_comment in All_comments:
            item['id']=musicid
            item['name'] = result
            # 用户名
            item['nickname'] = All_comment['user']['nickname'].replace(',', '，')
            # 用户ID
            item['userId'] = str(All_comment['user']['userId'])
            # 评论内容
            item['content'] = All_comment['content'].strip().replace('\n', '').replace(',', '，')
            yield item

