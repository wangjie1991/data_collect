# -*- coding: utf-8 -*-

import os
from pybloomfilter import BloomFilter


class LinkFilter():

    def __init__(self, name):
        self.name = name + ".bf"
        self.bf = BloomFilter(100000000, 0.01, self.name)
        '''
        if os.path.exists(self.name):
            self.bf = BloomFilter.open(self.name)
        else:
            self.bf = BloomFilter(100000000, 0.01, self.name)
        '''

    def link_filter(self, links):
        new_links = []
        for link in links:
            if not self.bf.add(link.url):
                new_links.append(link)
        return new_links


