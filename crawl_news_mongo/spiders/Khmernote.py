from abc import ABC

import scrapy
from ..items import NewsItem
from ..config import categoryProcess, convert_month_to_int, DebugMode, get_DateTime_by_crawl_time

from datetime import datetime
import pytz

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TEST_DATABASE
    col = db["Khmernote"]
else:
    db = client.OFFICIAL_DATABASE
    col = db["posts"]


class KhmernoteSpider(scrapy.Spider, ABC):
    # list_category_cambodia = []

    name = "Khmernote"

    list_categories = [
        "https://khmernote.com/news/category/nissan-auto-tech",
        "https://khmernote.com/news/category/%e1%9e%9f%e1%9e%bb%e1%9e%81%e1%9e%97%e1%9e%b6%e1%9e%96",
        "https://khmernote.com/news/category/news",
        # Link chua latest news
        # khi crawl url thi co dang khac, xu ly sau!
        # "https://khmernote.com/news-2",
        "https://khmernote.com/news/category/%e1%9e%9f%e1%9e%84%e1%9f%92%e1%9e%82%e1%9e%98",
        "https://khmernote.com/news/category/technology",
        "https://khmernote.com/news/category/pressrelease",
        "https://khmernote.com/news/category/national"
    ]

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    start_crawl_page = 1
    end_crawl_page = 9

    def start_requests(self):
        for category in self.list_categories:
            for page in range(self.start_crawl_page, self.end_crawl_page):
                page_category_to_crawl = category + "/page/{}".format(page)
                yield scrapy.Request(page_category_to_crawl, self.parse_category)

    def parse_category(self, response):
        image_list = response.xpath('//section[@id="category"]//div[@class="category__block__listsPic"]/a')
        for image in image_list:
            image_href = image.xpath('./@href').get()
            print("imageHREF", image_href)
            exist_url = False
            for x in col.find({"url": image_href}).limit(1):
                exist_url = True
                break
            if not exist_url:
                KhmernoteItem = NewsItem()
                KhmernoteItem['magazine'] = "Khmernote"
                KhmernoteItem['img'] = image.xpath('./img/@data-src').get()
                yield scrapy.Request(url=response.urljoin(image_href), callback=self.parse_content,
                                     meta={'Khmernote': KhmernoteItem})

    def parse_content(self, response):
        category = categoryProcess(response.xpath('//span[@class="single__content--cmnTag"]//text()').get().strip())

        # for cambodia_category in self.list_category_cambodia:
        #     if category == cambodia_category:
        #         break
        #     else:
        #         self.list_category_cambodia.append(category)

        if get_DateTime_by_crawl_time():
            date_with_timezone = datetime.now().replace(tzinfo=self.Cambodia_timezone)
        else:
            date = response.xpath('//span[@class="single__content--cmnDate"]//text()').get()
            date_with_timezone = datetime.strptime(date, "%B %d, %Y").replace(tzinfo=self.Cambodia_timezone)
        title = response.xpath('//div[@class="single__contentTitle"]//text()').get().strip()
        content = response.xpath('//div[@class="single__contentDetail"]').get()

        KhmernoteItem = response.meta.get('Khmernote')

        KhmernoteItem['category'] = category
        KhmernoteItem['title'] = title
        KhmernoteItem['content'] = content
        KhmernoteItem['date'] = date_with_timezone
        KhmernoteItem['url'] = response.url

        col.insert_one(KhmernoteItem)
        yield KhmernoteItem

    # print("listCategories", list_category_cambodia)

