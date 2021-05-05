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
    link = scrapy.Field()           #链接
    title = scrapy.Field()          #公告标题 采购项目
    category = scrapy.Field()       #品目
    content = scrapy.Field()        #公告正文
    
    pub_date = scrapy.Field()   #发布时间
    start_date = scrapy.Field()     #收标招标开始时间
    end_date = scrapy.Field()       #收标截止时间
    open_date = scrapy.Field()      #开标时间
    open_addr = scrapy.Field()      #开标地点

    bidder = scrapy.Field()         #招标人
    bidder_addr = scrapy.Field()    #招标人地址
    bidder_contact = scrapy.Field() #招标人联系方式
    contact_name = scrapy.Field()   #项目联系人
    contact_phone = scrapy.Field()  #项目联系电话
    agent_name = scrapy.Field()     #代理机构名称
    agent_addr = scrapy.Field()     #代理机构地址
    agent_contact = scrapy.Field()  #代理机构联系方式
    budget = scrapy.Field()         #预算金额
    
    area = scrapy.Field()           #地区
    province = scrapy.Field()       #省份
    # city = scrapy.Field()