import scrapy
from ..items import NewsItem
from datetime import datetime

from ..common import categoryProcess,convert_month_to_int,DebugMode

from pymongo import MongoClient


client = MongoClient('localhost',27017)

if DebugMode() == True:
    db = client.TEST_DATABASE
    col = db["Norkhothom"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]

class NorkhothomSpider(scrapy.Spider):
    name = "Norkhothom"

    list_categories = [
        'https://norkorthom.com/category/local-news/',
        'https://norkorthom.com/category/international-news/',
        'https://norkorthom.com/category/%e1%9e%96%e1%9f%90%e1%9e%8f%e1%9f%8c%e1%9e%98%e1%9e%b6%e1%9e%93%e1%9e%9f%e1%9e%b7%e1%9e%9b%e1%9f%92%e1%9e%94%e1%9f%88/',
        'https://norkorthom.com/category/international-sports/',
        'https://norkorthom.com/category/technology/',
        'https://norkorthom.com/category/beauty/',
        'https://norkorthom.com/category/%e1%9e%9f%e1%9e%bb%e1%9e%81%e1%9e%97%e1%9e%b6%e1%9e%96/',
        'https://norkorthom.com/category/report/'
    ]

    def start_requests(self):
        for category in self.list_categories:
            yield scrapy.Request(category,self.parse_category)

    def parse_category(self,response):
        urls = response.xpath('//div[@class="td-ss-main-content"]/div[@class="td-block-row"]/div/div/h3/a/@href').getall()

        for url in urls:
            exist_url = False
            for x in col.find({"url":url}).limit(1):
                exist_url = True
                break
            if exist_url == False:
                linkTitle = response.urljoin(url)
                yield scrapy.Request(url = linkTitle,callback=self.parse_content)
    def parse_content(self,response):
            time_title = response.xpath('//div[@class="td-post-header"]/header')
            title = time_title.xpath('./h1/text()').get()

            date = time_title.xpath('./div/span/time/text()').get()

            year = int(date.split()[2])
            month = convert_month_to_int(date.split()[0])
            day = int(date.split()[1].replace(",",""))

            date_in_iso_format = datetime(year,month,day)

            category = categoryProcess(response.xpath('//ul[@class="td-category"]/li/a/text()').get().strip())

            norItem = NewsItem()

            norItem['magazine'] = "Norkhothom"
            norItem['title'] = title
            norItem['date'] = date_in_iso_format
            norItem['category'] = category
            norItem['url'] = response.url
            # norItem['content'] = response.xpath('//div[@class="td-post-content"]').get()

            # col.find_one_and_update({'url':response.url},{'$set':{"category":category}})

            col.insert_one(norItem)

            yield norItem
