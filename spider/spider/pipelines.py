# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
    def process_item(self, item, spider):
        path = '../data/%s.txt' %s item['name']
        content = 'name=%s\nurl=%s\n' % (item['name'], item['url'])

        with open(path, 'w') as fout:
            fout.write(content)
        return item


