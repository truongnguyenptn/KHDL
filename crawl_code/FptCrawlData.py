from CrawlData import CrawlData
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from Config import Config

class FptCrawlData(CrawlData):
    DOMAIN = Config["FPT"]["DOMAIN"]
    DETAIL_LINK_FILE = Config["FPT"]["DETAIL_LINK_FILE"]
    RAW_DATA_FILE = Config["FPT"]["RAW_DATA_FILE"]

    def get_detail_links(self):
        self.driver.get(self.DOMAIN + "/may-tinh-xach-tay")
        sleep(2)

        # click btn load more to show all available products
        load_more_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-light")
        try:
            while load_more_btn is not None:
                load_more_btn.click()
                sleep(2)
                load_more_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-light")
        except Exception:
            pass

        # get detail links
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        link_details = []
        for a in soup.select(".cdt-product__info > h3 > a"):
            link_details.append(self.DOMAIN + a.get('href'))
        return link_details
    
    def get_info(self, link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        data = {}
        data['Title'] = soup.select_one('h1.st-name').get_text().strip().replace("\n", "") if soup.select_one('h1.st-name') else None
        data['Price sale'] = soup.select_one('.st-price__left .st-price-main').get_text() if soup.select_one('.st-price__left .st-price-main') else None
        data['Price origin'] = soup.select_one('.st-price__left .st-price-sub strike').get_text() if soup.select_one('.st-price__left .st-price-sub strike') else None

        for item in soup.select(".st-pd-table tr"):
            td = item.select("td")
            key = td[0].get_text()
            value = td[1].get_text()
            data[key] = value

        for item in soup.select(".c-modal__content .st-table tr"):
            td = item.select("td")
            key = td[0].get_text()
            value = td[1].get_text()
            data[key] = value
        for item in soup.select("#idata-3 .st-table tr"):
            td = item.select("td")
            key = td[0].get_text()
            value = td[1].get_text()
            data[key] = value

        data['url'] = link.replace("\n", "")
        return data

if __name__ == "__main__":
    crawler = FptCrawlData()
    crawler.exec()