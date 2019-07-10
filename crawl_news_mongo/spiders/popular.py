import scrapy
from ..items import NewsItem

from pymongo import MongoClient
import pdb

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['post_news']

class PopularSpider(scrapy.Spider):
    name = "popular"

    def start_requests(self):
        yield scrapy.Request('https://www.popular.com.kh/',self.parse)
    def parse(self, response):
        categories = response.xpath('//ul[@id="menu-top-menu"]/li/a')
        for category in categories:
            linkTitle = category.xpath('/text()').get()
            linkDest = response.urljoin(category.xpath('./@href').get())
            yield scrapy.Request(url=linkDest,callback=self.parse_category)
    def parse_category(self,response):
        urls = response.xpath('//ul[@class="mvp-blog-story-list left relative infinite-content"]/li/a/@href')
        for url in urls:
            linkUrl = response.urljoin(url.get())
            yield scrapy.Request(url=linkUrl,callback=self.parse_content)
    def parse_content(self,response):
        exist_url = False
        for x in col.find({"url":response.url}):
            exist_url = True
            break
        if exist_url == False:
            title = response.xpath('//header[@id="mvp-post-head"]/h1/text()').get()
            if title is None:
                print("NONE!!!!!")
            category = response.xpath('//header[@id="mvp-post-head"]/h3[@class="mvp-post-cat left relative"]/a/span/text()').get()
            if category == "កម្សាន្ត":
                category = "Entertainment"
            elif category == "ជីវិត & ការងារ":
                category = "Life Job"
            elif category == "ស្នេហាស្នេហ៍ហឺត":
                category = "Love"
            elif category == "សង្គម":
                category = "Social"
            elif category == "ទេសចរណ៍":
                category = "Tours"
            elif category == "កីឡា":
                category = "Sport"
            elif category == "បច្ចេកវិទ្យា":
                category = "Technology"
            elif category == "ចរាចរណ៍ថ្ងៃនេះ":
                category = "Traffic Today"

            date = response.xpath('//time[@class="post-date updated"]/text()').get()

            popularItem = NewsItem()

            popularItem['magazine'] = "Popular"
            popularItem['title'] = title
            popularItem['date'] = date
            popularItem['category'] = category
            popularItem['url'] = response.url
            popularItem['content'] = response.xpath('//div[@id="mvp-content-main"]').get()

            col.insert_one(popularItem)
            
            yield popularItem