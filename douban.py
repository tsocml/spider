# -*- coding: utf-8 -*-
import scrapy
class DoubanSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    introduce = scrapy.Field()
    star = scrapy.Field()
    describe = scrapy.Field()


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
    	movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
    	for i_item in movie_list:
    		douban_item = DoubanSpiderItem()
    		douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
    		douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
    		douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
    		yield douban_item
    	next_link = response.xpath("//span[@class='next']/link/@href").extract()
    	if next_link:
    		next_link = next_link[0]
    		yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback = self.parse)
        