import scrapy
from ..items import NewsItem

from pymongo import MongoClient
# import pdb

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['post_news']

class NorKhoThomSpider(scrapy.Spider):
    name = "norkhothom"

    def start_requests(self):
        yield scrapy.Request('https://norkorthom.com/',self.parse)
    def parse(self, response):
        categories = response.xpath('//div[@id="td-header-menu"]/div[@class="menu-main-menu-header-container"]/ul/li/a')

        for category in categories:
            linkCategory = response.urljoin(category.xpath('./@href').get())
            yield scrapy.Request(url=linkCategory,callback=self.parse_category)
    def parse_category(self,response):
        titles = response.xpath('//div[@class="td-ss-main-content"]/div[@class="td-block-row"]/div/div/h3/a')

        for title in titles:
            linkTitle = response.urljoin(title.xpath('./@href').get())
            yield scrapy.Request(url = linkTitle,callback=self.parse_content)
    def parse_content(self,response):
        exist_url = False
        for x in col.find({"url":response.url}):
            exist_url = True
            break
        if exist_url == False:

            time_title = response.xpath('//div[@class="td-post-header"]/header')
            title = time_title.xpath('./h1/text()').get()
            date = time_title.xpath('./div/span/time/text()').get()
            category = response.xpath('//ul[@class="td-category"]/li/a/text()').get()

            norItem = NewsItem()

            norItem['magazine'] = "Norkhothom"
            norItem['title'] = title
            norItem['date'] = date
            norItem['category'] = category
            norItem['url'] = response.url
            norItem['content'] = response.xpath('//div[@class="td-post-content"]').get()

            col.insert_one(norItem)

            yield norItem
