# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import NewsItem
from ..config import categoryProcess, convert_month_to_int, DebugMode

from datetime import datetime
import pytz

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TEST_DATABASE
    col = db["Khmerload"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]


class KhmerLoadSpider(scrapy.Spider):
    name = "Khmerload"

    list_category = [
        'https://www.khmerload.com/category/entertainment',
        'https://www.khmerload.com/category/social',
        'https://www.khmerload.com/category/sport',
        'https://www.khmerload.com/category/odd',
        'https://www.khmerload.com/category/health',
        'https://www.khmerload.com/category/tech',
        'https://www.khmerload.com/category/novel',
        'https://www.khmerload.com/category/knowledge'
    ]

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    def start_requests(self):
        for category in self.list_category:
            for page in range(1, 9):
                category_list_page = category + "?page={}".format(page)
                print(category_list_page)
                yield scrapy.Request(category_list_page, self.parse_test)

    def parse_test(self, response):
        image_with_hrefs = response.xpath('//div[@class="container homepage-wrap"]//div[@class="media"]/a')
        for image_with_href in image_with_hrefs:
            title_link = 'https://www.khmerload.com' + image_with_href.xpath('./@href').get()
            print(title_link)
            exist_url = False
            for x in col.find({"url": title_link}).limit(1):
                exist_url = True
                break
            if not exist_url:
                image_link = image_with_href.xpath('./img/@src').get()
                khmerloadItem = NewsItem()
                khmerloadItem['magazine'] = "Khmerload"
                khmerloadItem['img'] = image_link

                linkTitle = response.urljoin(title_link)
                yield scrapy.Request(url=linkTitle, callback=self.parse_content, meta={'test': khmerloadItem})
    #
    def parse_content(self, response):

        khmerloadItem = response.meta.get('test')

        title = response.xpath('//div[@class="article-header"]/h1//text()').get()
        date_and_time = response.xpath('((//div[@class="article-header-meta"]/div)[2]/text())[4]').get().replace("\n",
                                                                                                                 "").strip()

        # parse thoi gian
        year = int(date_and_time.split()[5])
        month = convert_month_to_int(date_and_time.split()[3])
        day = int(date_and_time.split()[4].replace(",", ""))

        time = date_and_time.split()[2]

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        date_in_date_format = datetime(year, month, day, hour, minute,tzinfo=self.Cambodia_timezone)

        # category tieng Anh
        category = categoryProcess(
            response.xpath('//li[@class="active"]/a/text()').get().replace("\n", "").replace(" ", "").strip())

        khmerloadItem['title'] = title
        khmerloadItem['date'] = date_in_date_format
        khmerloadItem['category'] = category
        khmerloadItem['url'] = response.url
        khmerloadItem['content'] = response.xpath('//div[@class="article-content"]').get()

        col.insert_one(khmerloadItem)

        yield khmerloadItem

# EXPORT RA JSON!
# process = CrawlerProcess({'FEED_URI': 'export.json',})
