# -*- coding: utf-8 -*-
import scrapy

from ..items import VideoItem
from ..config import DebugMode

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TESTDB
    col = db["Khmerload_video"]
else:
    db = client.OFFDB
    col = db["Video"]

class KhmerLoadVideoSpider(scrapy.Spider):
    name = 'KhmerloadVideoSpider'

    begin_link = 'https://www.khmerload.com/videos/show/'

    def start_requests(self):
        for category_number in range(1,17):
            for page in range (1,10):
                link_to_page = self.begin_link + "{}".format(category_number) + "?page={}".format(page)
                yield scrapy.Request(link_to_page,self.parse_video_page)

    def parse_video_page(self,response):
        list_video_url = response.xpath('//div[@class="video-preview-list"]/a/@href').getall()
        for video_url in list_video_url:
            video_url = "https://www.khmerload.com"+video_url.split("?")[0]
            # if(col.count_documents({"url":video_url},limit = 1) == 0):
            yield scrapy.Request(video_url,self.parse_video)

    def parse_video(self,response):
        f = open("video.txt","a+")

        video_crawl_area = response.xpath('.//div[@class="container"]')
        iframe_link = video_crawl_area.xpath('.//iframe/@src').get().strip()
        video_detail = video_crawl_area.xpath('.//div[@class="detail"]')
        video_category = video_detail.xpath('./span[@id="kicker"]/text()').get().strip()


        # video_descriptions = video_detail.xpath('./p//text()').getall()
        # for description in video_descriptions:
        #     description = description.strip()
        #     if(description!=""):
        #         video_description = description
        #         break

        # video_description = video_detail.xpath('./p[@id="description"]//text()').get().strip()
        # if(video_description==""):
        #     f.write(response.url + "\n")

        # f.write(video_detail.xpath('.//p[@id="description"]/following-sibling::*[1]').get()+"\n")
        # f.write(video_detail.xpath('.//p[@id="description"]/following-sibling::*[1]').getall()+"\n")

        video_description = video_detail.xpath('.//p[@id="description"]/following-sibling::*[1]')
        
        # if(len(video_description.xpath('./p').getall()) == 0):
        #     # f.write(video_description.xpath('./p/text()').get() + "\n")
        #     f.write(response.url + "\n")

        video_title = video_detail.xpath('./a[@id="title"]/text()').get().strip()

        khmerloadVideoItem = VideoItem()
        khmerloadVideoItem['magazine'] = "Khmerload"
        khmerloadVideoItem['url'] = response.url
        khmerloadVideoItem['iframe_src'] = iframe_link
        khmerloadVideoItem['category'] = video_category
        khmerloadVideoItem['description'] = video_description.get()
        khmerloadVideoItem['title'] = video_title

        col.insert_one(khmerloadVideoItem)

        yield khmerloadVideoItem


