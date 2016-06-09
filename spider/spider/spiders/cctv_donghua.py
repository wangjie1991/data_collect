# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import SpiderItem


class CctvDonghuaSpider(CrawlSpider):
    name = 'cctv_donghua'
    start_urls = ['http://donghua.cctv.com']
    allowed_domains = [ 'donghua.cctv.com', ]
    linkfilter = LinkFilter('cctv_donghua')

    allow_page = [ r'http://donghua.cctv.com.*' ]
    #deny_pages = [ r'http://sports\.sina\.com\.cn/focus//.*', ]

    rules = [  Rule(LinkExtractor(allow=allow_shtml), callback='parse_item', 
                    follow=True, process_links=linkfilter.html_filter)
            ]

    def parse_item(self, response):
        item = SpiderItem()

        flcvd = Flcvd(url)
        flcvd_urls = flcvd.parse()

        ps = response.xpath('//div[@id="artibody"]//p')
        if not ps:
            ps = response.xpath('//div[@id="article"]//p')

        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)
        
        return item


