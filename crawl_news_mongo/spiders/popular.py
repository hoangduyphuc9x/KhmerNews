import scrapy
from ..items import NewsItem
from datetime import datetime

from pymongo import MongoClient

from ..common import categoryProcess,convert_month_to_int,DebugMode

client = MongoClient('localhost',27017)

if DebugMode() == True:
    db = client.TEST_DATABASE
    col = db["Popular"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]

class PopularSpider(scrapy.Spider):
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
        'https://www.popular.com.kh/category/bii2019/'
    ]

    def start_requests(self):
        for category in self.list_categories:
            yield scrapy.Request(category,self.parse_category)

    def parse_category(self,response):
        urls = response.xpath('//ul[@class="mvp-blog-story-list left relative infinite-content"]/li/a/@href').getall()
        for url in urls:
            exist_url = False
            for x in col.find({"url":url}).limit(1):
                exist_url = True
                break
            if exist_url == False:
                linkUrl = response.urljoin(url)
                yield scrapy.Request(url=linkUrl,callback=self.parse_content)

    def parse_content(self,response):
        title = response.xpath('//header[@id="mvp-post-head"]/h1/text()').get()
        if title is None:
            print("NONE!!!!!")
        category = categoryProcess(response.xpath('//header[@id="mvp-post-head"]/h3[@class="mvp-post-cat left relative"]/a/span/text()').get().strip())

        date = response.xpath('//time[@class="post-date updated"]/text()').get()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[0])
        day = int(date.split()[1].replace(",",""))

        date_in_iso_format = datetime(year,month,day)

        popularItem = NewsItem()

        popularItem['magazine'] = "Popular"
        popularItem['title'] = title
        popularItem['date'] = date_in_iso_format
        popularItem['category'] = category
        popularItem['url'] = response.url
        # popularItem['content'] = response.xpath('//div[@id="mvp-content-main"]').get()

        col.insert_one(popularItem)

        # col.find_one_and_update({"category":None},{'$set':{"category":"POP FEED"}})

        yield popularItem