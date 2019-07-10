# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import NewsItem

from pymongo import MongoClient
import pdb

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['post_news']

class KhmerLoadSpider(scrapy.Spider):

    name = "khmerload"
    
    def start_requests(self):
        yield scrapy.Request('https://www.khmerload.com/',self.parse)

    def parse(self, response):
        categories = response.xpath('//nav[@id="nav-main"]//li//a')
        for category in categories:
            LinkTitle = category.xpath('/text()').get()
            
            LinkDest = response.urljoin(category.xpath('./@href').get())
            yield scrapy.Request(url=LinkDest, callback=self.parse_category)
    def parse_category(self,response):
        titles = response.xpath('//div[@class="content"]')
        
        for title in titles:
            linkTitle = response.urljoin(title.xpath('.//@href').get())
            yield scrapy.Request(url=linkTitle,callback = self.parse_content)
    def parse_content(self,response):
        exist_url = False
        for x in col.find({"url":response.url}):
            exist_url = True
            break
        if exist_url == False:
                title = response.xpath('//div[@class="article-header"]/h1//text()').get()
                if title is None:
                    print("NONE!!!!")
                date = response.xpath('((//div[@class="article-header-meta"]/div)[2]/text())[4]').get().replace("\t","")
                category = response.xpath('//li[@class="active"]/a/text()').get().replace("\n","").replace(" ","")

                if category == "តារា&កម្សាន្ដ":
                    category = "Star & Entertainment"
                elif category == "សង្គម":
                    category = "Social"
                elif category == "កីទ្បា":
                    category = "Sport"
                elif category == "ប្លែកៗ":
                    category = "Odd"
                elif category == "សម្រស់&សុខភាព":
                    category = "Beautiful & Health"
                elif category == "យល់ដឹង":
                    category = "Knowledge"
                elif category == "បច្ចេកវិទ្យា":
                    category = "Technology"
                elif category == "ប្រលោមលោក&អប់រំ":
                    category = "Novel & Education"

                newsItem = NewsItem()

                # newsItem['_id'] = 1
                newsItem['magazine'] = "Khmerload"
                newsItem['title'] = title
                newsItem['date'] = date
                newsItem['category'] = category
                newsItem['url'] = response.url
                newsItem['content'] = response.xpath('//div[@class="article-content"]').get()

                col.insert_one(newsItem)

                yield newsItem

#EXPORT RA JSON!
# process = CrawlerProcess({'FEED_URI': 'export.json',})