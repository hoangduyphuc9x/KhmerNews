import scrapy
from ..items import NewsItem

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
# col = db['Kohsantepheapdaily']
col = db['posts']

class KohsantepheapdailySpider(scrapy.Spider):
    name = "Kohsantepheapdaily"

    list_category = [
        'https://kohsantepheapdaily.com.kh/category/local',
        'https://kohsantepheapdaily.com.kh/category/security',
        'https://kohsantepheapdaily.com.kh/category/local-news',
        'https://kohsantepheapdaily.com.kh/category/politic',
        'https://kohsantepheapdaily.com.kh/category/agriculture',
        'https://kohsantepheapdaily.com.kh/category/traffic',
        'https://kohsantepheapdaily.com.kh/category/opinion',
        'https://kohsantepheapdaily.com.kh/category/environment',
        'https://kohsantepheapdaily.com.kh/category/economic',
        'https://kohsantepheapdaily.com.kh/category/international',
        'https://kohsantepheapdaily.com.kh/category/today-in-history',
        'https://kohsantepheapdaily.com.kh/category/international-news',
        'https://kohsantepheapdaily.com.kh/category/world-economy',
        'https://kohsantepheapdaily.com.kh/category/sport',
        'https://kohsantepheapdaily.com.kh/category/local-sport',
        'https://kohsantepheapdaily.com.kh/category/international-sport',
        'https://kohsantepheapdaily.com.kh/category/world-cup',
        'https://kohsantepheapdaily.com.kh/category/art-culture',
        'https://kohsantepheapdaily.com.kh/category/proverb',
        'https://kohsantepheapdaily.com.kh/category/relax',
        'https://kohsantepheapdaily.com.kh/category/religious',
        'https://kohsantepheapdaily.com.kh/category/tourism',
        'https://kohsantepheapdaily.com.kh/category/culture',
        'https://kohsantepheapdaily.com.kh/category/entetaintment',
        'https://kohsantepheapdaily.com.kh/category/classify',
        'https://kohsantepheapdaily.com.kh/category/auto',
        'https://kohsantepheapdaily.com.kh/category/realestates',
        'https://kohsantepheapdaily.com.kh/category/health',
        'https://kohsantepheapdaily.com.kh/category/healthiness',
        'https://kohsantepheapdaily.com.kh/category/services',
        'https://kohsantepheapdaily.com.kh/category/advertisement',
        'https://kohsantepheapdaily.com.kh/category/charity',
        'https://kohsantepheapdaily.com.kh/category/research',
        'https://kohsantepheapdaily.com.kh/category/knowledge',
        'https://kohsantepheapdaily.com.kh/category/technology',
        'https://kohsantepheapdaily.com.kh/category/funny',
        'https://kohsantepheapdaily.com.kh/category/local-weather',
        'https://kohsantepheapdaily.com.kh/category/research-docs',
        'https://kohsantepheapdaily.com.kh/category/horoscope',
        'https://kohsantepheapdaily.com.kh/category/jobs']

    def start_requests(self):
        for category in self.list_category:
            for page in range (1,9):
                category_list_page = category + '/page/{}'.format(page)
                # print(category_list_page)

                yield scrapy.Request(category_list_page,self.parse_category)

    def parse_category(self,response):
        articles = response.xpath("/html/body/section/div[2]/div//div[@class='image-box']/a/@href").getall()
        for article in articles:
            exist_url = False
            for x in col.find({"url":article}).limit(1):
                exist_url = True
            if exist_url == False:
                yield response.follow(url=article,callback=self.parse_content)
    def parse_content(self,response):

        head = response.xpath("/html/body/div[7]/div/div[1]")
        newsItem = NewsItem()

        newsItem['magazine'] = "Kohsantepheapdaily"
        newsItem['title'] = head.xpath("./h1/text()").get()
        newsItem['url'] = response.url
        newsItem['category'] = "Dang Cap Nhat"
        newsItem['date'] = head.xpath("./ul[1]/li[1]/time/text()").get()

        col.insert_one(newsItem)

        yield newsItem


