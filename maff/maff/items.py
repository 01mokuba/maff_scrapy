# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArchiveItem(scrapy.Item):
    links = scrapy.Field()
    month = scrapy.Field()


class ClipItem(scrapy.Item):
    src = scrapy.Field()
    text = scrapy.Field()
    attachments = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
