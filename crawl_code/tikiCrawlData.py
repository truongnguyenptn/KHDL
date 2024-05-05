from CrawlData import CrawlData
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from Config import Config

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': 'k2QERlHIBzdrmhW4yYcPtaMDn5Sv9qCj',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

# tham số truyền vào 
params_laptop = {
    'limit': '48',
    'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
    'aggregations': '1',
    'trackity_id': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
    'category': '8095',
    'page': '1',
    'src': 'c8095',
    'urlKey':  'laptop',
}

class tikiCrawlData(CrawlData):
    DOMAIN = Config["TIKI"]["DOMAIN"]
    DETAIL_LINK_FILE = Config["TIKI"]["DETAIL_LINK_FILE"]
    RAW_DATA_FILE = Config["TIKI"]["RAW_DATA_FILE"]

    def get_detail_links(self):
        link_details = []
        for page in range(1, 19):
            s = f"{self.DOMAIN}/laptop/c8095?page={page}"
            html = requests.get(s, headers=headers, params=params_laptop)
            bs = BeautifulSoup(html.text, features="html.parser")
            for a in bs.select("a.product-item"):
                link_details.append(f"{self.DOMAIN}{a['href']}")
            sleep(1)

        return link_details
    
    def get_info(self, link):
        self.driver.get(link)
        sleep(1)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        data = {}
        data['Title'] = soup.select_one('h1').get_text().strip().replace("\n", "") if soup.select_one('h1') else None
        data['Price sale'] = soup.select_one('.product-price__current-price').get_text().strip() if soup.select_one('.product-price__current-price') else None
        data['discount rate'] = soup.select_one('.product-price__discount-rate').get_text().strip() if soup.select_one('.product-price__discount-rate') else None
        for item in soup.select(".WidgetTitle__WidgetContentRowStyled > span"):
            print(item)
           
        data['url'] = link.replace("\n", "")
        return data

if __name__ == "__main__":
    crawler = tikiCrawlData()
    crawler.exec(True)