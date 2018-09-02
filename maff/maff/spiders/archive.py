# -*- coding: utf-8 -*-

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from maff.items import ArchiveItem, ClipItem


class ArchiveSpider(CrawlSpider):
    name = 'archive'
    allowed_domains = [
        'www.maff.go.jp', 'www.rinya.maff.go.jp'
        'www.affrc.maff.go.jp', 'www.jfa.maff.go.jp'
    ]
    start_urls = ['http://www.maff.go.jp/j/press/arc/index.html']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(
            allow=['http://www.maff.go.jp/j/press/arc/[\d]+\.html'],
            restrict_xpaths=['//div[@class=\'content\']']
        ), callback='parse_archive_list', follow=True),
        Rule(LinkExtractor(
            allow=['http://www.rinya.maff.go.jp/j/press/.*'],
            restrict_xpaths=['//div[@class=\'area2\']']
        ), callback='parse_rinya', follow=True),
        Rule(LinkExtractor(
            allow=['http://www.maff.go.jp/j/press/.*'],
            restrict_xpaths=['//div[@class=\'area2\']']
        ), callback='parse_rinya', follow=True),
        Rule(LinkExtractor(
            allow=['http://www.jfa.maff.go.jp/j/press/.*'],
            restrict_xpaths=['//div[@class=\'content\']']
        ), callback='parse_jfa', follow=True),
    )

    def parse_archive_list(self, response):
        item = ArchiveItem()
        item['links'] = []
        item['month'] = response.url.split('/')[-1].replace('.html', '')
        for linkitem in response.xpath('//div[@class=\'content\']//a'):
            item['links'].append({
                'href': linkitem.xpath('@href').extract_first(),
                'text': linkitem.xpath('text()').extract_first()
            })
        return item

    def parse_rinya(self, response):
        item = ClipItem()
        item['src'] = response.xpath('//body').extract_first()
        content_root = response.xpath('//div[@class=\'area2\']')
        item['text'] = content_root.extract_first()
        item['attachments'] = []
        item['file_urls'] = []
        for d in response.xpath('//a'):
            dd = d.xpath('@href').extract_first()
            if dd is not None:
                if re.match('^https?://', dd) is None:
                    dd = response.urljoin(dd)
                if re.match('.*\.[Pp][Dd][Ff]$', dd) is not None:
                    item['attachments'].append({
                        'href': dd,
                        'text': d.xpath('text()').extract_first()
                    })
                    item['file_urls'].append(dd)
        return item

    def parse_jfa(self, response):
        item = ClipItem()
        item['src'] = response.xpath('//body').extract_first()
        content_root = response.xpath('//div[@class=\'content\']')
        item['text'] = content_root.extract_first()
        item['attachments'] = []
        item['file_urls'] = []
        for d in response.xpath('//a'):
            dd = d.xpath('@href').extract_first()
            if dd is not None:
                if re.match('^https?://', dd) is None:
                    dd = response.urljoin(dd)
                if re.match('.*\.[Pp][Dd][Ff]$', dd) is not None:
                    item['attachments'].append({
                        'href': dd,
                        'text': d.xpath('text()').extract_first()
                    })
                    item['file_urls'].append(dd)
        return item
