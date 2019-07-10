# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    magazine = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
