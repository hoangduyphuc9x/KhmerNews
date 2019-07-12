import scrapy
from scrapy.crawler import CrawlerProcess

from .khmerload import KhmerLoadSpider
from .norkhothom import NorKhoThomSpider
from .todaysharing import TodaysharingSpider
from .dapnews import DapnewsSpider
from .popular import PopularSpider

process = CrawlerProcess()
process.crawl(KhmerLoadSpider)
process.crawl(PopularSpider)
process.crawl(TodaysharingSpider)
process.crawl(DapnewsSpider)
process.crawl(NorKhoThomSpider)
process.start()