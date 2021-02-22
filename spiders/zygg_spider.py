import scrapy


class ZyggSpiderSpider(scrapy.Spider):
    name = 'zygg_spider'
    allowed_domains = ['http://www.ccgp.gov.cn/cggg/zygg/gkzb/']
    start_urls = ['http://http://www.ccgp.gov.cn/cggg/zygg/gkzb//']

    def parse(self, response):
        pass
