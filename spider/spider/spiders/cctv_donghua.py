# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from spider.spiders.linkfilter import LinkFilter
from spider.spiders.flvcd import Flvcd
from spider.items import SpiderItem


class CctvDonghuaSpider(CrawlSpider):
    name = 'cctv_donghua'
    start_urls = ['http://donghua.cctv.com']
    linkfilter = LinkFilter('cctv_donghua')
    allowed_domains = [ 'donghua.cctv.com', 'donghua.cntv.cn',
                        'tv.cctv.com', 'tv.cntv.cn' ]

    allow_index = [ r'http://donghua.cctv.com.*', r'http://donghua.cntv.cn.*' ]
    allow_vida =  [ r'http://tv.cctv.com/\d{4}/\d{2}/\d{2}/VIDA\w+.shtml' ]
    allow_item =  [ r'http://tv.cctv.com/\d{4}/\d{2}/\d{2}/VIDE\w+.shtml',
                    # http://tv.cctv.com/2016/03/28/VIDErJCd2VVkgDiVer9EuaRT160328.shtml
                    r'http://tv.cntv.cn/video/.*',
                    #http://tv.cntv.cn/video/C36571/62faf66977f84996bde70fe74c3808b3
                  ]

    rules = [  Rule(LinkExtractor(allow=allow_index), follow=True,
                    process_links=linkfilter.link_filter),
               Rule(LinkExtractor(allow=allow_vida), callback='parse_vida',
                    follow=False, process_links=linkfilter.link_filter),
               Rule(LinkExtractor(allow=allow_item), callback='parse_item',
                    follow=False, process_links=linkfilter.link_filter)
            ]

    pat_vida_url = re.compile(r"'url':'(.*?)'")

    def parse_vida(self, response):
        body = response.body.decode('utf8')
        urls = self.pat_vida_url.findall(body)
        reqs = []
        for url in urls:
            req = scrapy.Request(url)
            reqs.append(req)
        return reqs

    def parse_item(self, response):
        item = SpiderItem()
        title = response.xpath('//title/text()').extract()[0]
        if title == 'CNTV.cn_ERROR':
            return None
        flvcd = Flvcd(response.url)
        flvcd_url = flvcd.parse()
        if not flvcd_url:
            return None
        item['name'] = title[:title.find('_')]
        item['url'] = response.url
        item['flvcd'] = flvcd_url
        return item


