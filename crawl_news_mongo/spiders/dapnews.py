# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from pymongo import MongoClient
from ..common import categoryProcess,convert_month_to_int,DebugMode
from datetime import datetime

client = MongoClient('localhost',27017)

if DebugMode() == True:
    db = client.TEST_DATABASE
    col = db["Dap_news"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]

class DapNewsSpider(scrapy.Spider):
    name = 'dapnews'

    list_categories = [
        'https://www.dap-news.com/latest-news',
        'https://www.dap-news.com/archives/category/national',
        'https://www.dap-news.com/archives/category/national/politic',
        'https://www.dap-news.com/archives/category/national/society',
        'https://www.dap-news.com/archives/category/international',
        'https://www.dap-news.com/archives/category/realestate',
        'https://www.dap-news.com/archives/category/biography',
        'https://www.dap-news.com/archives/category/sports',
        'https://www.dap-news.com/archives/category/entertainment',
        'https://www.dap-news.com/archives/category/health'
    ]

    def start_requests(self):
        for category in self.list_categories:
            yield scrapy.Request(category,self.parse_category)

    def parse_category(self,response):
        url_news = response.xpath('//div[@id="archive-list-wrap"]/ul/li/a/@href').getall()
        for url in url_news:
            exist_url = False
            for x in col.find({"url":url}).limit(1):
                exist_url = True
            if exist_url == False:
                get_content_with_url = response.urljoin(url)
                yield scrapy.Request(url=get_content_with_url,callback=self.parse_content)

    def parse_content(self,response):
        article = response.xpath('//article[@id="post-area"]')

        category = categoryProcess(article.xpath('./header/a/span/text()').get().strip())
        title = article.xpath('./header/h1/text()').get()

        date_and_time = article.xpath('(./header/div/div/div/div/div)[2]/span[@class="post-date updated"]/time/text()').get()

        date = date_and_time.split("|")[0].strip()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[1])
        day = int(date.split()[0])

        time = date_and_time.split("|")[1].strip()
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        date_in_iso_format = datetime(year,month,day,hour,minute)

        # post_feat_img = ""
        # if(article.xpath('./div[@id="post-feat-img"]') is not None):
        #     post_feat_img = article.xpath('./div[@id="post-feat-img"]').get()
        # content = article.xpath('./div[@id="content-area"]').get() + post_feat_img

        dapsItem = NewsItem()

        dapsItem['magazine'] = "DapNews"
        dapsItem['title'] = title
        dapsItem['date'] = date_in_iso_format
        dapsItem['category'] = category
        dapsItem['url'] = response.url
        # dapsItem['content'] = content

        # col.find_one_and_update({'url':response.url},{'$set':{"date":date,"time":time,"category":category}})
        col.insert_one(dapsItem)
        yield dapsItem

