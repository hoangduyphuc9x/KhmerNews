# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem


class HealthSpider(scrapy.Spider):
    name = 'health'
    
    def start_requests(self):
        yield scrapy.Request('https://www.health.com.kh',self.parse)

    def parse(self, response):
        categories = response.xpath('(//div[@class="menu-illnesslist-container"])[1]/ul/li/a/@href')
        categories_child = (response.xpath('(//div[@class="menu-illnesslist-container"])[1]/ul/li/ul/li/a/@href'))

        for cat in categories:
                
            test = NewsItem()

            test['title'] = cat.get()

            yield test

        for cat in categories_child:
                
            test = NewsItem()

            test['title'] = cat.get()

            yield test
