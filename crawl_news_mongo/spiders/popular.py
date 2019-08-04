# Cai thien toc do:
# Lay category, title, image ngay o buoc parse_category

from abc import ABC

import scrapy
from ..items import NewsItem
from datetime import datetime
import pytz

from pymongo import MongoClient

from ..config import categoryProcess, convert_month_to_int, DebugMode

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TEST_DATABASE
    col = db["Popular"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]


class PopularSpider(scrapy.Spider, ABC):
    name = "popular"

    list_categories = [
        'https://www.popular.com.kh/category/entertainment/',
        'https://www.popular.com.kh/category/lifejob/',
        'https://www.popular.com.kh/category/love/',
        'https://www.popular.com.kh/category/social/',
        'https://www.popular.com.kh/category/tours/',
        'https://www.popular.com.kh/category/sport/',
        'https://www.popular.com.kh/category/technology/',
        'https://www.popular.com.kh/category/traffic-today/',
        'https://www.popular.com.kh/category/pop-feed/',
        'https://www.popular.com.kh/category/bii2019/',
        'https://www.popular.com.kh/category/dengte/'
    ]

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    def start_requests(self):
        for category in self.list_categories:
            for page in range(1, 9):
                category_list_page = category + "page/{}".format(page)
                yield scrapy.Request(category_list_page, self.parse_category)

    def parse_category(self, response):

        urls = response.xpath('//ul[@class="mvp-blog-story-list left relative infinite-content"]/li/a/@href').getall()
        for url in urls:
            exist_url = False
            for x in col.find({"url": url}).limit(1):
                exist_url = True
                break
            if not exist_url:
                print(response.url)
                linkUrl = response.urljoin(url)
                yield scrapy.Request(url=linkUrl, callback=self.parse_content)

    def parse_content(self, response):
        # print("parse content " + response.url)
        title = response.xpath('//header[@id="mvp-post-head"]/h1/text()').get()
        if title is None:
            print("NONE!!!!!")
        category = categoryProcess(response.xpath('//header[@id="mvp-post-head"]/h3[@class="mvp-post-cat left '
                                                  'relative"]/a/span/text()').get().strip())

        date = response.xpath('//time[@class="post-date updated"]/text()').get()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[0])
        day = int(date.split()[1].replace(",", ""))

        date_in_iso_format = datetime(year, month, day,tzinfo=self.Cambodia_timezone)
        print("ISO FORMAT")
        print(date_in_iso_format)

        popularItem = NewsItem()

        popularItem['magazine'] = "Popular"
        popularItem['title'] = title
        popularItem['date'] = date_in_iso_format
        popularItem['category'] = category
        popularItem['url'] = response.url
        popularItem['content'] = response.xpath('//div[@id="mvp-content-main"]').get()

        # anh nay to, co the load bi cham!!!!!!!!!!!!
        popularItem['img'] = response.xpath('//div[@id="mvp-post-feat-img"]/img/@src').get()

        col.insert_one(popularItem)

        # # col.find_one_and_update({"category":None},{'$set':{"category":"POP FEED"}})

        yield popularItem
