from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from gentest1.items import Gentest1Item
from scrapy.conf import settings

class SpiderMan(Spider):
    name = 'linkgen'
    documents = {
        "stackoverflow": {"allow_url": 'stackoverflow.com', "start_url": 'http://stackoverflow.com/questions/tagged/html'},
        "wikipedia": {"allow_url": 'wikipedia.org', "start_url": 'http://en.wikipedia.org/wiki/HTML'},
        "w3schools": {"allow_url": 'w3schools.com', "start_url": 'http://www.w3schools.com/html/'},
        "freelancer": {"allow_url": 'freelancer.com', "start_url": 'https://www.freelancer.com/jobs/HTML.1/1/'},
        "meetup": {"allow_url": 'meetup.com', "start_url": 'http://html.meetup.com'}
    }
    allowed_domains = []
    start_urls = []
    
    def __init__(self):
        #settings.overrides['DEPTH_LIMIT'] = 0
        settings.set('ITEM_PIPELINES', {'gentest1.pipelines.Gentest1Pipeline':1000})
        settings.set('LOG_FILE', 'log.txt')
        for n,d in self.documents.iteritems():
            self.allowed_domains.append(d['allow_url'])
            self.start_urls.append(d['start_url'])
        #self._rules = (Rule(LxmlLinkExtractor(allow=self.allowed_domains), callback=self.parse_page, follow=False),)
    
    def start_requests(self):
        ret_val = []
        for n,d in self.documents.iteritems():
            requests = self.make_requests_from_url(d['start_url'])
            requests.meta['document_name'] = n
            ret_val.append(requests)
        return ret_val
    
    #def parse_start_url(self, response):
    #    self.item = Gentest1Item()
    #    self.item['url'] = response.url
    #    self.item['document_name'] = response.xpath('//title/text()').extract()[0]
    #    return self.item
    
    #def parse_page(self, response):
    #    #for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
    #    #    self.item['url_list'].append(link.url)
    #    #self.item['url_list'].append(response.url)
    #    self.item['url'] = response.url
    #    return self.item
    
    def parse(self, response):
        items = []
        for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
            item = Gentest1Item()
            item['url'] = link.url
            item['document_name'] = response.meta['document_name']
            items.append(item)
            requests = self.make_requests_from_url(link.url)
            requests.meta['document_name'] = response.meta['document_name']
            items.append(requests)
        return items

