import scrapy


class DfggSpiderSpider(scrapy.Spider):
    name = 'dfgg_spider'
    allowed_domains = ['ccgp.gov.cn']
    start_urls = ['http://www.ccgp.gov.cn/cggg/dfgg/gkzb/index.htm']

    def parse(self, response):
        pass
