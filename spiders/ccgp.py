import scrapy


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['search.ccgp.gov.cn']
    start_urls = ['http://search.ccgp.gov.cn/bxsearch?searchtype=1&bidSort=1&pinMu=3&bidType=1&dbselect=bidx&start_time=2020%3A08%3A27&end_time=2021%3A02%3A25&timeType=5&pppStatus=0&page_index=1']

    def parse(self, response):
        pass
