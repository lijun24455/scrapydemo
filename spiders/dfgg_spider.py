import scrapy
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..items import BidItem

def request_url(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

class DfggSpiderSpider(scrapy.Spider):
    name = 'dfgg_spider'
    allowed_domains = ['ccgp.gov.cn']
    start_urls = ['http://www.ccgp.gov.cn/cggg/dfgg/gkzb/index.htm']
    cur_index = 1

    def parse(self, response):
        print('current url:' + response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        bid_list = soup.find(class_= 'vF_detail_relcontent_lst').find_all('li')
        for bid_item in bid_list:
            item = BidItem()

            item_href = bid_item.find('a').get('href')
            item_title = bid_item.find('a').get('title')
            item_date = bid_item.find_all('em')[0].get_text()
            item_publisher = bid_item.find_all('em')[-1].get_text()

            item_content_html = request_url(response.urljoin(item_href))
            item_content_soup = BeautifulSoup(item_content_html)
            item_content = item_content_soup.find(class_ = 'vF_deail_maincontent').get_text(" ", strip=True)

            item['link'] = response.urljoin(item_href)
            item['title'] = item_title
            item['publisher'] = item_publisher
            item['date'] = item_date
            item['content'] = item_content
            yield item
        
        next_url = response.urljoin('index_' + str(self.cur_index) + '.htm')
        self.cur_index = self.cur_index + 1
        if self.cur_index > 24:
            return
        yield scrapy.Request(url=next_url, callback=self.parse)
    
