# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class DBScrapyItem(scrapy.Item):
    username = scrapy.Field()
    userlink = scrapy.Field()
    comment_time = scrapy.Field()
    useful_count = scrapy.Field()
    comment = scrapy.Field()

