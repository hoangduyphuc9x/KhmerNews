# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from ..config import categoryProcess, convert_month_to_int, DebugMode,get_DateTime_by_crawl_time

from datetime import datetime
import pytz

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TESTDB
    col = db["Khmerload"]
else:
    db = client.OFFDB
    col = db["posts"]


class KhmerLoadSpider(scrapy.Spider):

    name = "Khmerload"

    #co cai nay nua :v Chia ra lam Khmer Star, Chinese Star,.........
    # https://www.khmerload.com/interest/%E1%9E%8F%E1%9E%B6%E1%9E%9A%E1%9E%B6%E1%9E%81%E1%9F%92%E1%9E%98%E1%9F%82%E1%9E%9A
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
    end_crawl_page = 2

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    def start_requests(self):
        for category in self.list_category:
            for page in range(self.start_crawl_page, self.end_crawl_page):
                category_list_page = category + "?page={}".format(page)
                print(category_list_page)
                #o day cho quay vong duoc ko?
                yield scrapy.Request(category_list_page, self.parse_test)

    def parse_test(self, response):
        #Chon cac bai bao xuat hien
        image_with_hrefs = response.xpath('//div[@class="column-idx-1"or@class="column-idx-2"or@class="column-idx-0"]//a[./img]')
        for image_with_href in image_with_hrefs:
            link_to_content = "https://www.khmerload.com"+image_with_href.xpath('./@href').get()
            if(col.count_documents({"url":link_to_content},limit=1)!=0):
                break
            else:
                khmerloadItem = NewsItem()
                khmerloadItem['magazine'] = "Khmerload"
                khmerloadItem['url'] = link_to_content
                khmerloadItem['img'] = "https:" + image_with_href.xpath('./img/@src').get()
                yield response.follow(link_to_content,callback=self.parse_content,meta={"khmerload":khmerloadItem})

    def parse_content(self, response):

        khmerloadItem = response.meta.get('khmerload')

        title = response.xpath('//div[@class="article-header"]/h1//text()').get()

        if get_DateTime_by_crawl_time():
            date_with_timezone = datetime.now().replace(tzinfo=self.Cambodia_timezone)
        else:
            date_and_time = response.xpath('((//div[@class="article-header-meta"]/div)[2]/text())[4]').get().replace("\n","").strip()
            dateTime = date_and_time.split()[2]+" "+date_and_time.split()[3]+" "+date_and_time.split()[4]+" "+date_and_time.split()[5]
            date_with_timezone = datetime.strptime(dateTime,"%H:%M %B %d, %Y").replace(tzinfo=self.Cambodia_timezone)

        content = ("<html><head><style>img{max-width: 100%; width:auto; height: auto;}"+
            "figcaption{color:gray;font-size:.8rem;padding-left:10px;text-align:center;}"+
            "figure{margin:0,margin-top:1rem}"+
            "p{font-size:1.2rem}"+"</style></head><body><div>")

        content_raw = response.xpath('//div[@class="article-content"]/div[1]/*[local-name()="figure" or local-name()="p"]').getall()
        for raw in content_raw:
            content = content + raw
        content = content + "</div></body></html>"

        # category tieng Anh
        category = categoryProcess(
            response.xpath('//li[@class="active"]/a/text()').get().replace("\n", "").replace(" ", "").strip())

        khmerloadItem['title'] = title
        khmerloadItem['date'] = date_with_timezone
        khmerloadItem['category'] = category
        khmerloadItem['url'] = response.url
        khmerloadItem['content'] = content

        col.insert_one(khmerloadItem)

        yield khmerloadItem

# EXPORT RA JSON!
# process = CrawlerProcess({'FEED_URI': 'export.json',})
