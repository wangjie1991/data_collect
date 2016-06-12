# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
    idx = 0

    def process_item(self, item, spider):
        self.idx += 1
        path = '../data/%s.txt' % str(self.idx)
        content = 'name=%s\nurl=%s\nflvcd=%s\n' % \
                  (item['name'], item['url'], item['flvcd'])

        with open(path, 'w') as fout:
            fout.write(content.encode('utf8'))

        with open('../data/flvcd.txt', 'a') as fout:
            urls = item['flvcd'].split('|')
            for url in urls:
                fout.write(url + '\n')

        return item


