# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class Gentest1Pipeline(object):
    
    url_dict = {}
    num_spiders = 1
    max_len = 200
    
    def process_item(self, item, spider):
        #print "-----RECEIVE ITEM-----"
        if item['document_name'] in self.url_dict:
            if len(self.url_dict[item['document_name']]) >= self.max_len:
                u = spider.documents[item['document_name']]['allow_url']
                if u in spider.allowed_domains:
                    print "------Remove Item----- " + u
                    spider.allowed_domains.remove(u)
                    self.flush_content()
            else:
                if item['url'] not in self.url_dict[item['document_name']]:
                    self.url_dict[item['document_name']].append(item['url'])
        else:
            self.url_dict[item['document_name']] = [item['url']]
        return item
    
    def close_spider(self, spider):
        self.num_spiders = self.num_spiders - 1
        if self.num_spiders == 0:
            print "***********HERE*************"
            self.flush_content()
    
    def flush_content(self):
        with open('test2.txt', 'w') as outfile:
            json.dump(self.url_dict, outfile, indent=2)