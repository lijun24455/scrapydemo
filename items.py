# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class ScrapydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BidItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    publisher = scrapy.Field()
    date = scrapy.Field()

class SrchResultItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    publisher = scrapy.Field()
    date = scrapy.Field()
    province = scrapy.Field()
    sort = scrapy.Field()