# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['post_news']


class TodaysharingSpider(scrapy.Spider):
    name = 'todaysharing'
    
    def start_requests(self):
        yield scrapy.Request('http://news.todaysharing.com/',self.parse)
    def parse(self, response):
        categories = response.xpath('//ul[@id="main-navigation"]//@href')

        for category in categories:
            cate = response.urljoin(category.get())
            yield scrapy.Request(url=cate,callback=self.parse_category)
    def parse_category(self,response):
        links = response.xpath('//div[@class="listing listing-blog listing-blog-5 clearfix "]/article/div/h2/a/@href')
        for link in links:
            linkTitle = response.urljoin(link.get())
            yield scrapy.Request(url=linkTitle,callback=self.parse_content)
    def parse_content(self,response):
        exist_url = False
        for x in col.find({"url":response.url}):
            exist_url = True
            break
        if exist_url == False:
            title = response.xpath('//article//h1/span/text()').get()
            date = response.xpath('//article//time/b/text()').get()
            content = response.xpath('//article/div[@class="entry-content clearfix single-post-content"]').get()
            category = response.xpath('//ul[@class="bf-breadcrumb-items"]/li[2]/a/span/text()').get()

            todaySharingItem = NewsItem()

            todaySharingItem['magazine'] = "Todaysharing"
            todaySharingItem['title'] = title
            todaySharingItem['date'] = date
            todaySharingItem['url'] = response.url
            todaySharingItem['content'] = content
            todaySharingItem['category'] = category

            col.insert_one(todaySharingItem)
            
            yield todaySharingItem
