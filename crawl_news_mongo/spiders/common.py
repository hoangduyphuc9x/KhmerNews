import scrapy
from scrapy.crawler import CrawlerProcess

from .khmerload import KhmerLoadSpider
from .norkhothom import NorkhothomSpider
from .todaysharing import TodaySharingSpider
from .dapnews import DapnewsSpider
from .popular import PopularSpider

process = CrawlerProcess()
process.crawl(KhmerLoadSpider)
# process.crawl(PopularSpider)
process.crawl(TodaySharingSpider)
# process.crawl(DapnewsSpider)
# process.crawl(NorKhoThomSpider)
process.start()