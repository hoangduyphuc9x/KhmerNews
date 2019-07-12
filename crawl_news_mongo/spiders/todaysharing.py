# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['TodaySharing']

class TodaySharingSpider(scrapy.Spider):
    name = 'todaysharing'

    list_category = [
        'http://news.todaysharing.com/category/knowledge/',
        'http://news.todaysharing.com/category/real-estate/',
        'http://news.todaysharing.com/category/entertainment/',
        'http://news.todaysharing.com/category/health-beauty/',
        'http://news.todaysharing.com/category/economic/',
        'http://news.todaysharing.com/category/sports/',
        'http://news.todaysharing.com/categoryclear/lifestyle/',
        'http://news.todaysharing.com/category/news/'
    ]
    
    def start_requests(self):
        for category in self.list_category:
            for i in range (1,9):
                category_page = category + "page/{}".format(i)
                yield scrapy.Request(category_page,self.parse_category)

    def parse_category(self,response):
        links = response.xpath('//div[@class="listing listing-blog listing-blog-5 clearfix "]/article/div/h2/a/@href').getall()
        for link in links:
            exist_url = False
            for x in col.find({"url":link}).limit(1):
                exist_url = True
                break
            if exist_url == False:
                yield scrapy.Request(url=response.urljoin(link),callback=self.parse_content)
    def parse_content(self,response):

        title = response.xpath('//article//h1/span/text()').get()
        date = response.xpath('//article//time/b/text()').get()
        content = response.xpath('//article/div[@class="entry-content clearfix single-post-content"]').get()
        category = response.xpath('//ul[@class="bf-breadcrumb-items"]/li[2]/a/span/text()').get()

        todaySharingItem = NewsItem()

        todaySharingItem['magazine'] = "TodaySharing"
        todaySharingItem['title'] = title
        todaySharingItem['date'] = date
        todaySharingItem['url'] = response.url
        todaySharingItem['content'] = content
        todaySharingItem['category'] = category

        col.insert_one(todaySharingItem)

        yield todaySharingItem