import scrapy
from scrapy.crawler import CrawlerProcess

from .khmerload import KhmerLoadSpider
from .norkhothom import NorkhothomSpider
from .todaysharing import TodaySharingSpider
from .dapnews import DapNewsSpider
from .popular import PopularSpider
from .kohsantepheapdaily import KohsantepheapdailySpider

process = CrawlerProcess()
process.crawl(KhmerLoadSpider)
process.crawl(PopularSpider)
# process.crawl(TodaySharingSpider)
process.crawl(DapNewsSpider)
# process.crawl(NorkhothomSpider)
# process.crawl(KohsantepheapdailySpider)
process.start()