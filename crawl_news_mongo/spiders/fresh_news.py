# -*- coding: utf-8 -*-
import scrapy


class FreshNewsSpider(scrapy.Spider):
    name = 'fresh_news'

    def parse(self, response):
        pass
