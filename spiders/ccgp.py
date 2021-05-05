# -*- coding: utf-8 -*-

import scrapy
import requests
import re
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scrapy_splash import SplashRequest
import sys
print(sys.path)
from ..items import SrchResultItem


headers_list = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]


def request_url(url):
    header = random.choice(headers_list)
    kv = {'user-agent': header}
    try:
        response = requests.get(url, headers = kv, timeout = 30)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print('请求失败，statusCode:', response.status_code)
            return None
    except requests.RequestException:
        return None


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['search.ccgp.gov.cn']
    start_urls = ['http://search.ccgp.gov.cn/bxsearch?searchtype=1&bidSort=0&pinMu=0&bidType=1&dbselect=bidx&kw=&page_index=1&start_time=2021%3A05%3A01&end_time=2021%3A05%3A04&timeType=1']
   
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait':1}, headers={'user-agent':random.choice(headers_list)})

    def parse(self, response):
        print('[current url]:' + response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        result_list_segment_soup = soup.find(class_= 'vT-srch-result-list-bid')
        if(result_list_segment_soup == None):
            print('未找到列表!!!')
        else:
            result_list = result_list_segment_soup.find_all('li')
            for result_item in result_list:
                item = SrchResultItem()

                item_href = result_item.find('a').get('href')
                item_title = result_item.find('a').get_text().strip()
                item_content = result_item.find('span').get_text('', strip=True).replace('\r','').replace('\n','')

                pub_province = item_content.split('|')[3].strip()

                #请求子页面
                item_detail_html = request_url(item_href)
                item_detail_soup = BeautifulSoup(item_detail_html)
                item_detail_content = item_detail_soup.find(class_ = 'vF_detail_content').get_text('', strip=True)
                item_table = item_detail_soup.find('table')
                for td in item_table.find_all(class_ = 'title'):
                    key = td.get_text('', strip=True)
                    value = td.find_next().get_text('', strip=True)
                    if('品目' in key):
                        item['category'] = value
                    if('采购单位' == key):
                        item['bidder'] = value
                    if('行政区域' in key):
                        item['area'] = value
                    if('公告时间' in key):
                        item['pub_date'] = value
                    if('开标时间' in key):
                        item['open_date'] = value
                    if('开标地点' in key):
                        item['open_addr'] = value
                    if('预算' in key):
                        item['budget'] = value
                    if('项目联系人' in key):
                        item['contact_name'] = value
                    if('项目联系电话' in key):
                        item['contact_phone'] = value
                    if('采购单位地址' == key):
                        item['bidder_addr'] = value
                    if('采购单位联系方式' == key):
                        item['bidder_contact'] = value
                    if('代理机构名称' in key):
                        item['agent_name'] = value
                    if('代理机构地址' in key):
                        item['agent_addr'] = value
                    if('代理机构联系方式' in key):
                        item['agent_contact'] = value 
                item['title'] = item_title
                item['link'] = response.urljoin(item_href)
                item['content'] = item_detail_content
                item['province'] = pub_province
                yield item
        
            pager_next_onclick = soup.find(class_ = 'pager').find(class_ = 'next').get('onclick')
            if(pager_next_onclick != None):
                next_page_index = re.findall(r'[(](.*?)[)]', pager_next_onclick)[0]
                print('next_pager_index:', next_page_index)
                next_url = re.sub(r'page_index=\d+', 'page_index='+next_page_index, response.url)

                yield SplashRequest(url=next_url, callback=self.parse, args={'wait':3}, headers={'user-agent':random.choice(headers_list)})
            else:
                print('Scrapy parse finish!')

        
        
