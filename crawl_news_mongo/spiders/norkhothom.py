import scrapy
from ..items import NewsItem
from datetime import datetime
import pytz
from ..config import categoryProcess, convert_month_to_int, DebugMode

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TESTDB
    col = db["Norkhothom"]
else:
    db = client.OFFDB
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

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    def start_requests(self):
        for category in self.list_categories:
            yield scrapy.Request(category, self.parse_category)

    def parse_category(self, response):
        urls = response.xpath(
            '//div[@class="td-ss-main-content"]/div[@class="td-block-row"]/div/div/h3/a/@href').getall()

        for url in urls:
            if(col.count_documents({"url":url},limit=1)==0):
                img_src = response.xpath('//div[@class="td-module-image"]//img/@src').get()
                norItem = NewsItem()
                norItem['img'] = img_src
                linkTitle = response.urljoin(url)
                yield scrapy.Request(url=linkTitle, callback=self.parse_content, meta={"norItem":norItem})

    def parse_content(self, response):
        time_title = response.xpath('//div[@class="td-post-header"]/header')
        title = time_title.xpath('./h1/text()').get()

        date = time_title.xpath('./div/span/time/text()').get()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[0])
        day = int(date.split()[1].replace(",", ""))

        date_in_iso_format = datetime(year, month, day, tzinfo=self.Cambodia_timezone)

        category = categoryProcess(response.xpath('//ul[@class="td-category"]/li/a/text()').get().strip())

        img_content_list = []
        img_content = response.xpath('//div[@class="td-post-content"]//img')
        for img in img_content:
            src_img = img.xpath('./@src').get()
            if(src_img is not None and len(img_content_list)<=2):
                img_content_list.append(src_img)

        norItem = response.meta.get("norItem")

        if(norItem['img'] is None):
            if(len(img_content_list)>0):
                norItem['img'] = img_content_list[0]

        norItem['magazine'] = "Norkhothom"
        norItem['title'] = title
        norItem['date'] = date_in_iso_format
        norItem['category'] = category
        norItem['url'] = response.url
        norItem['content_img'] = img_content_list
        norItem['views'] = 0
        # norItem['content'] = response.xpath('//div[@class="td-post-content"]').get()

        # col.find_one_and_update({'url':response.url},{'$set':{"category":category}})

        col.insert_one(norItem)

        yield norItem
