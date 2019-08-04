# -*- coding: utf-8 -*-

# TOC DO KHA CHAM!!!!

from abc import ABC

import scrapy
from ..items import NewsItem
from pymongo import MongoClient
from ..config import categoryProcess, convert_month_to_int, DebugMode
from datetime import datetime
import pytz

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TEST_DATABASE
    col = db["Dap_news"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]


class DapNewsSpider(scrapy.Spider, ABC):
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
    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    page_start_to_crawl = 1
    page_end_to_crawl = 9

    def start_requests(self):
        for category in self.list_categories:
            for page in range(self.page_start_to_crawl, self.page_end_to_crawl):
                category_list_page = category + "/page/{}".format(page)
                yield scrapy.Request(category_list_page, self.parse_category)

    def parse_category(self, response):
        list_post = response.xpath('//li[@class="infinite-post"]')
        list_news_link = list_post.xpath('./a')
        for news_link in list_news_link:
            link_href = news_link.xpath('./@href').get()
            exist_url = False
            for x in col.find({"url": link_href}).limit(1):
                exist_url = True
                break
            if not exist_url:
                list_image = news_link.xpath('.//img/@src').get()
                dapNewsItem = NewsItem()
                dapNewsItem['magazine'] = "DapNews"
                dapNewsItem['img'] = list_image
                dapNewsItem['url'] = link_href
                dapNewsItem['title'] = news_link.xpath('./@title').get()
                get_content_with_url = response.urljoin(link_href)
                yield scrapy.Request(url=get_content_with_url, callback=self.parse_content,
                                     meta={'dapNewsMeta': dapNewsItem})

    def parse_content(self, response):

        dapNewsItem = response.meta.get('dapNewsMeta')
        article = response.xpath('//article[@id="post-area"]')

        category = categoryProcess(article.xpath('./header/a/span/text()').get().strip())
        # title = article.xpath('./header/h1/text()').get()

        date_and_time = article.xpath(
            '(./header/div/div/div/div/div)[2]/span[@class="post-date updated"]/time/text()').get()

        date = date_and_time.split("|")[0].strip()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[1])
        day = int(date.split()[0])

        time = date_and_time.split("|")[1].strip()
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        date_in_iso_format = datetime(year, month, day, hour, minute,tzinfo=self.Cambodia_timezone)

        # post_feat_img = ""
        if article.xpath('./div[@id="post-feat-img"]') is not None:
            post_feat_img = article.xpath('./div[@id="post-feat-img"]').get()
        content = article.xpath('./div[@id="content-area"]').get() + post_feat_img

        # dapNewsItem['title'] = title
        dapNewsItem['date'] = date_in_iso_format
        dapNewsItem['category'] = category
        dapNewsItem['content'] = content

        # col.find_one_and_update({'url':response.url},{'$set':{"date":date,"time":time,"category":category}})
        col.insert_one(dapNewsItem)
        yield dapNewsItem
