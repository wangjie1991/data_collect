# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import SpiderItem


class IqiyiSpider(CrawlSpider):
    name = 'iqiyi'
    start_urls = ['http://www.iqiyi.com']
    linkfilter = LinkFilter('iqiyi')

    allowed_domains = [ 'gongyi.sina.com.cn', ]
    deny_pages = [ r'http://sports\.sina\.com\.cn/focus//.*', ]
    allow_index = [ r'http://news.jiaju.sina.com.cn/.*', ]
    allow_shtml = [ r'http://cul\.history\.sina\.com.\cn/.*\.s?html$', ]

    rules = [ Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
            ]

    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)
        item = SpiderItem()

        loader.add_value('path', path)
        loader.add_xpath('text', '//h1/text()')
        
        ps = response.xpath('//div[@id="artibody"]//p')
        if not ps:
            ps = response.xpath('//div[@id="article"]//p')

        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)
        
        return loader.load_item()


