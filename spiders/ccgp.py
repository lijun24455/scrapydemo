import scrapy


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['www.ccgp.gov.cn']
    start_urls = ['http://www.ccgp.gov.cn/']

    def parse(self, response):
        pass
