# Cai thien toc do:
# Lay category, title, image ngay o buoc parse_category

from abc import ABC

import scrapy
from ..items import NewsItem
from datetime import datetime
import pytz

from pymongo import MongoClient

from ..config import categoryProcess, convert_month_to_int, DebugMode

client = MongoClient('localhost', 27017)

if DebugMode():
    db = client.TESTDB
    col = db["Popular"]
else:
    db = client.OFFDB
    col = db["posts"]


class PopularSpider(scrapy.Spider, ABC):
    name = "popular"

    list_categories = [
        'https://www.popular.com.kh/category/entertainment/',
        'https://www.popular.com.kh/category/lifejob/',
        'https://www.popular.com.kh/category/love/',
        'https://www.popular.com.kh/category/social/',
        'https://www.popular.com.kh/category/tours/',
        'https://www.popular.com.kh/category/sport/',
        'https://www.popular.com.kh/category/technology/',
        'https://www.popular.com.kh/category/traffic-today/',
        'https://www.popular.com.kh/category/pop-feed/',
        'https://www.popular.com.kh/category/bii2019/',
        'https://www.popular.com.kh/category/dengte/'
    ]

    Cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')

    start_page_crawl = 1
    end_page_crawl = 9

    def start_requests(self):
        for category in self.list_categories:
            for page in range(self.start_page_crawl, self.end_page_crawl):
                category_list_page = category + "page/{}".format(page)
                yield scrapy.Request(category_list_page, self.parse_category)

    def parse_category(self, response):
        a_tags_with_href_and_image = response.xpath('//li/a[.//img]')
        for a_tag in a_tags_with_href_and_image:
            if(col.count_documents({"url":a_tag.xpath('./@href').get()},limit = 1)==0):
                url_to_content = a_tag.xpath('./@href').get()
                popularItem = NewsItem()
                popularItem['magazine'] = "Popular"
                popularItem['url'] = url_to_content
                popularItem['img'] = a_tag.xpath('.//img[1]/@src').get()
                popularItem['views'] = 0
                yield response.follow(url_to_content,callback=self.parse_content,meta={"popular":popularItem})

    def parse_content(self, response):
        popularItem = response.meta.get('popular')

        title = response.xpath('//header[@id="mvp-post-head"]/h1/text()').get()

        category = categoryProcess(response.xpath('//header[@id="mvp-post-head"]/h3//span/text()').get().strip())

        date = response.xpath('//time[@class="post-date updated"]/text()').get()

        year = int(date.split()[2])
        month = convert_month_to_int(date.split()[0])
        day = int(date.split()[1].replace(",", ""))

        date_in_iso_format = datetime(year, month, day,tzinfo=self.Cambodia_timezone)

        # #-------------------CONTENT-------------------
        # #css, style,....
        # css_head_html = ("<html><head><style>img{max-width: 100%; width:auto; height: auto;margin:0}\n"+
        #     "iframe{width:100%; height:100%;}</style></head><body>")
        # # Lay src anh va video duoc nhung o dau bai
        # pre_image_and_video = ""
        # video_and_image_embed = response.xpath('//div[@id="mvp-video-embed" or @id="mvp-post-feat-img"]//*[local-name() = ("iframe" or "img")][1]')
        # for ifr in video_and_image_embed:
        #     if(ifr.xpath('name()').get() == 'iframe'):
        #         pre_image_and_video = pre_image_and_video + "<iframe src=\"" +  ifr.xpath('./@src').get() + "\"></iframe>\n"
        #     else:
        #         pre_image_and_video = pre_image_and_video + "<img src= \"" +  ifr.xpath('./@src').get() + "\"></img>\n"
        # content = css_head_html + pre_image_and_video
        # content_list_with_p_tag = response.xpath('//div[@id="mvp-content-main"]/p').getall()
        # for p_tag in content_list_with_p_tag:
        #     content = content + p_tag
        # content = content + "</body></html>"
        # #---------------------END CONTENT-----------------

        # #------------------------IMAGE-CONTENT-----------------------
        list_img_content = []

        prelude_images = response.xpath('//div[@id="mvp-post-feat-img"]//img/@src')
        for pre_image in prelude_images:
            if(pre_image.get() is not None and len(list_img_content) <= 2):
                list_img_content.append(pre_image.get())
                
        content_images_src = response.xpath('//div[@id="mvp-content-main"]//img/@src')
        for images_src in content_images_src:
            if(images_src.get() is not None and len(list_img_content) <= 2):
                list_img_content.append(images_src.get())
        
        # #--------------------------END-IMAGE-CONTENT---------------------------
 
        popularItem['title'] = title
        popularItem['date'] = date_in_iso_format
        popularItem['category'] = category
        popularItem['content_img'] = list_img_content

        # popularItem['content'] = content

        # anh nay to, co the load bi cham!!!!!!!!!!!!
        # popularItem['img'] = response.xpath('//div[@id="mvp-post-feat-img"]/img/@src').get()

        # # col.find_one_and_update({"category":None},{'$set':{"category":"POP FEED"}})

        col.insert_one(popularItem)
        yield popularItem
