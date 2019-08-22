import scrapy
from scrapy.crawler import CrawlerProcess

from .khmerload import KhmerLoadSpider
from .norkhothom import NorkhothomSpider
from .todaysharing import TodaySharingSpider
from .dapnews import DapNewsSpider
from .popular import PopularSpider
from .Khmernote import KhmernoteSpider
from .kohsantepheapdaily import KohsantepheapdailySpider

from .KhmerloadVideo import KhmerLoadVideoSpider

process = CrawlerProcess()
process.crawl(KhmerLoadSpider)
process.crawl(PopularSpider)
process.crawl(TodaySharingSpider)
process.crawl(DapNewsSpider)
# # Norkhothom can request AJAX de load them bai bao.....
process.crawl(NorkhothomSpider)
# Cai nay chua lam list_img_content
process.crawl(KhmernoteSpider)
# process.crawl(KohsantepheapdailySpider)
# process.crawl(KhmerLoadVideoSpider)
process.start()