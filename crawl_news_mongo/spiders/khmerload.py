# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from ..config import categoryProcess, convert_month_to_int, DebugMode,get_DateTime_by_crawl_time

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

    start_crawl_page = 1
    end_crawl_page = 9

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    def start_requests(self):
        for category in self.list_category:
            for page in range(self.start_crawl_page, self.end_crawl_page):
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

    def parse_content(self, response):

        khmerloadItem = response.meta.get('test')

        title = response.xpath('//div[@class="article-header"]/h1//text()').get()

        if get_DateTime_by_crawl_time():
            date_with_timezone = datetime.now().replace(tzinfo=self.Cambodia_timezone)
        else:
            date_and_time = response.xpath('((//div[@class="article-header-meta"]/div)[2]/text())[4]').get().replace("\n","").strip()
            dateTime = date_and_time.split()[2]+" "+date_and_time.split()[3]+" "+date_and_time.split()[4]+" "+date_and_time.split()[5]
            date_with_timezone = datetime.strptime(dateTime,"%H:%M %B %d, %Y").replace(tzinfo=self.Cambodia_timezone)

        # category tieng Anh
        category = categoryProcess(
            response.xpath('//li[@class="active"]/a/text()').get().replace("\n", "").replace(" ", "").strip())

        khmerloadItem['title'] = title
        khmerloadItem['date'] = date_with_timezone
        khmerloadItem['category'] = category
        khmerloadItem['url'] = response.url
        khmerloadItem['content'] = response.xpath('//div[@class="article-content"]').get()

        col.insert_one(khmerloadItem)

        yield khmerloadItem

# EXPORT RA JSON!
# process = CrawlerProcess({'FEED_URI': 'export.json',})
