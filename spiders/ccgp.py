import scrapy
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..items import BidItem, SrchResultItem

def request_url(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['search.ccgp.gov.cn']
    start_urls = ['http://search.ccgp.gov.cn/bxsearch?searchtype=1&bidSort=1&pinMu=3&bidType=1&dbselect=bidx&start_time=2020%3A08%3A27&end_time=2021%3A02%3A25&timeType=5&pppStatus=0&page_index=1']

    def parse(self, response):
        print('current url:' + response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        result_list = soup.find(class_= 'vT-srch-result-list-bid').find_all('li')
        for result_item in result_list:
            item = SrchResultItem()

            item_href = result_item.find('a').get('href')
            item_title = result_item.find('a').get_text().strip()
            item_content = result_item.find('span').get_text('', strip=True).replace('\r','').replace('\n','')

            pub_date = item_content.split('|')[0].strip()
            publisher = item_content.split('|')[1].strip()
            pub_agent = item_content.split('|')[2].strip()
            pub_province = item_content.split('|')[3].strip()
            pub_sort = item_content.split('|')[-1].strip()

            item_detail_html = request_url(item_href)
            item_detail_soup = BeautifulSoup(item_detail_html)
            item_detail_content = item_detail_soup.find(class_ = 'vF_detail_maincontent').get_text('', strip=True)

            item['link'] = response.urljoin(item_href)
            item['title'] = item_title
            item['publisher'] = publisher
            item['date'] = pub_date
            item['content'] = item_detail_content
            item['province'] = pub_province
            item['sort'] = pub_sort
            yield item
        
        pager_segment = soup.find(class_ = 'pager')
        page_next_index = pager_segment.find('')


        next_url = response.urljoin('index_' + str(self.cur_index) + '.htm')
        self.cur_index = self.cur_index + 1
        if self.cur_index > 24:
            return
