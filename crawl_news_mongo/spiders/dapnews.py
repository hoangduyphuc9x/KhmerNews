# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from pymongo import MongoClient
import pdb

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['post_news']


class DapnewsSpider(scrapy.Spider):
    name = 'dapnews'
    
    def start_requests(self):
        yield scrapy.Request('https://www.dap-news.com/',self.parse)

    def parse(self, response):
        categories = response.xpath('//ul[@id="menu-main-menu"]//li/a/@href')
        del categories[-1]

        for category in categories:
            linkCategory = response.urljoin(category.get())
            yield scrapy.Request(url=linkCategory,callback=self.parse_category)
    def parse_category(self,response):
        titles = response.xpath('//div[@id="archive-list-wrap"]/ul/li/a/@href')
        for title in titles:
            linkTitle = response.urljoin(title.get())
            yield scrapy.Request(url=linkTitle,callback=self.parse_content)


    def parse_content(self,response):
        exist_url = False
        for x in col.find({"url":response.url}):
            exist_url = True
            break
        if exist_url == False:

            article = response.xpath('//article[@id="post-area"]')

            category = article.xpath('./header/a/span/text()').get()
            title = article.xpath('./header/h1/text()').get()
            date = article.xpath('(./header/div/div/div/div/div)[2]/span[@class="post-date updated"]/time/text()').get()
            post_feat_img = ""
            if(article.xpath('./div[@id="post-feat-img"]') is not None):
                post_feat_img = article.xpath('./div[@id="post-feat-img"]').get()
            content = article.xpath('./div[@id="content-area"]').get() + post_feat_img

            dapsItem = NewsItem()

            dapsItem['magazine'] = "DapNews"
            dapsItem['title'] = title
            dapsItem['date'] = date
            dapsItem['category'] = category
            dapsItem['url'] = response.url
            dapsItem['content'] = content
            
            col.insert_one(dapsItem)
            yield dapsItem

