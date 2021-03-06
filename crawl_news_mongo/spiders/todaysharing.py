# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem

from pymongo import MongoClient

from ..config import categoryProcess, convert_month_to_int, DebugMode
from datetime import datetime

client = MongoClient('localhost', 27017)

if DebugMode() == True:
    db = client.TESTDB
    col = db["TodaySharing"]
else:
    db = client.OFFDB
    col = db["posts"]


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

    start_crawl_page = 1
    end_crawl_page = 9

    def start_requests(self):
        for category in self.list_category:
            for i in range(self.start_crawl_page, self.end_crawl_page):
                category_page = category + "page/{}".format(i)
                yield scrapy.Request(category_page, self.parse_category)

    def parse_category(self, response):
        links = response.xpath(
            '//div[@class="listing listing-blog listing-blog-5 clearfix "]/article/div/h2/a/@href').getall()
        for link in links:
            if(col.count_documents({"url":link},limit=1)==0):
                todaySharingItem = NewsItem()
                todaySharingItem['img'] = response.xpath('//div[@class="listing listing-blog listing-blog-5 clearfix "]/article/div//div[@class="featured clearfix"]/a/@data-src').get()
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_content,meta={"todaySharing":todaySharingItem})

    def parse_content(self, response):

        todaySharingItem = response.meta.get("todaySharing")

        title = response.xpath('//article//h1/span/text()').get()
        date = response.xpath('//article//time/b/text()').get()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[0])
        day = int(date.split()[1].replace(",", ""))

        date_in_iso_format = datetime(year, month, day)
        # content = response.xpath('//article/div[@class="entry-content clearfix single-post-content"]').get()
        category = categoryProcess(
            response.xpath('//ul[@class="bf-breadcrumb-items"]/li[2]/a/span/text()').get().replace("\n", "").replace(
                "\t", "").strip())

        list_content_img = []
        list_img_src = response.xpath('//div[contains(@class,"single-post-content")]/*[local-name()!="div"]//img')
        for img in list_img_src:
            if(len(list_content_img) <= 2):
                if(img.xpath('./@src').get() is not None):
                    list_content_img.append(img.xpath('./@src').get())
                elif(img.xpath('./@data-src').get() is not None):
                    list_content_img.append(img.xpath('./@data-src').get())

        if(todaySharingItem['img'] is None):
            if(len(list_content_img) > 0):
                todaySharingItem['img'] = list_content_img[0]

        todaySharingItem['magazine'] = "TodaySharing"
        todaySharingItem['title'] = title
        todaySharingItem['date'] = date_in_iso_format
        todaySharingItem['url'] = response.url
        # todaySharingItem['content'] = content
        todaySharingItem['category'] = category
        todaySharingItem['content_img'] = list_content_img
        todaySharingItem['views'] = 0

        col.insert_one(todaySharingItem)

        yield todaySharingItem
