# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import NewsItem
from ..common import categoryProcess,convert_month_to_int,DebugMode

from datetime import datetime

from pymongo import MongoClient

client = MongoClient('localhost',27017)

if DebugMode() == True:
    db = client.TEST_DATABASE
    col = db["Khmerload"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]

class KhmerLoadSpider(scrapy.Spider):

    name = "Khmerload"

    def start_requests(self):
        yield scrapy.Request('https://www.khmerload.com/',self.parse)

    def parse(self, response):
        categories = response.xpath('//nav[@id="nav-main"]//li//a')
        for category in categories:
            LinkDest = response.urljoin(category.xpath('./@href').get())
            yield scrapy.Request(url=LinkDest, callback=self.parse_category)

    def parse_category(self,response):

        # homepage = response.xpath('//div[@class="homepage-zone-1"]')
        # main_title_news = response.xpath('//div[class="homepage-zone-4"]')

        list_pages = response.xpath('//ul[@class="pagination"]/li[position()<10]/a/@href').getall()

        for list_page in list_pages:
            yield response.follow(url=list_page,callback=self.parse_test)

    def parse_test(self, response):
        titles = response.xpath('//div[@class="homepage-zone-4"]/div/ul/li/article/div[2]/a/@href').getall()
        for title in titles:
            title = 'https://www.khmerload.com' + title
            exist_url = False
            for x in col.find({"url":title}).limit(1):
                exist_url = True
                break
            if exist_url == False:
                linkTitle = response.urljoin(title)
                yield scrapy.Request(url=linkTitle,callback = self.parse_content)

    def parse_content(self,response):
        title = response.xpath('//div[@class="article-header"]/h1//text()').get()
        date_and_time = response.xpath('((//div[@class="article-header-meta"]/div)[2]/text())[4]').get().replace("\n","").strip()

        #parse thoi gian
        year = int(date_and_time.split()[5])
        month = convert_month_to_int(date_and_time.split()[3])
        day = int(date_and_time.split()[4].replace(",",""))

        time = date_and_time.split()[2]

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        date_in_date_format = datetime(year,month,day,hour,minute)

        #category tieng Anh
        category = categoryProcess(response.xpath('//li[@class="active"]/a/text()').get().replace("\n","").replace(" ","").strip())

        newsItem = NewsItem()

        newsItem['magazine'] = "Khmerload"
        newsItem['title'] = title
        newsItem['date'] = date_in_date_format
        newsItem['category'] = category
        newsItem['url'] = response.url
        # newsItem['content'] = response.xpath('//div[@class="article-content"]').get()

        col.insert_one(newsItem)

        yield newsItem


#EXPORT RA JSON!
# process = CrawlerProcess({'FEED_URI': 'export.json',})
