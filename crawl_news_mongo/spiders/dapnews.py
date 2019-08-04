# -*- coding: utf-8 -*-

# TOC DO KHA CHAM!!!!

from abc import ABC

import scrapy
from ..items import NewsItem
from pymongo import MongoClient
from ..config import categoryProcess, DebugMode, get_DateTime_by_crawl_time
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

        # category = categoryProcess(article.xpath('./header/a/span/text()').get().strip())

        category = categoryProcess(response.xpath('//header[@id="post-header"]//span/text()').get().strip())
        if get_DateTime_by_crawl_time():
            date_with_timezone = datetime.now().replace(tzinfo=self.Cambodia_timezone)
        else:
            date_and_time = response.xpath('//time[@itemprop="datePublished"]/text()').get()
            date_with_timezone = datetime.strptime(date_and_time, "%d %B %Y | %H:%M").replace(tzinfo=self.Cambodia_timezone)

        pre_image = response.xpath('//div[@id="post-feat-img"]/img').get()
        if(pre_image is not None):
            pre_image = "<center>" + pre_image + "</center>";
        content_pre = response.xpath('//div[@id="content-main"]/*[local-name()!="div" and local-name()!="style"]').getall()
        result_content = ""
        for content in content_pre:
            result_content = result_content+content
        if pre_image is not None:
            result_content = pre_image + result_content

        dapNewsItem['date'] = date_with_timezone
        dapNewsItem['category'] = category
        dapNewsItem['content'] = result_content

        # col.find_one_and_update({'url':response.url},{'$set':{"date":date,"time":time,"category":category}})
        col.insert_one(dapNewsItem)
        yield dapNewsItem
