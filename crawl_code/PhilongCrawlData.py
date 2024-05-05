from CrawlData import CrawlData
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from Config import Config

class PhilongCrawlData(CrawlData):
    DOMAIN = Config["PHILONG"]["DOMAIN"]
    DETAIL_LINK_FILE = Config["PHILONG"]["DETAIL_LINK_FILE"]
    RAW_DATA_FILE = Config["PHILONG"]["RAW_DATA_FILE"]

    def get_detail_links(self):
        link_details = []
        for page in range(1, 21):
            html = requests.get(f"{self.DOMAIN}/may-tinh-xach-tay.html?page={page}")
            bs = BeautifulSoup(html.text, features="html.parser")
            for a in bs.select("#product_item_in_list > div > div > a.p-img"):
                link_details.append(f"{self.DOMAIN}{a['href']}")
            sleep(1)

        return link_details
    
    def get_info(self, link):
        self.driver.get(link)
        sleep(1)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        data = {}
        data['Title'] = soup.select_one('.entry-header > h1').get_text().strip().replace("\n", "") if soup.select_one('.entry-header > h1') else None
        data['Price sale'] = soup.select_one('.p-price > span').get_text().strip() if soup.select_one('.p-price > span') else None
        data['Price origin'] = soup.select_one('.p-unprice> span').get_text().strip() if soup.select_one('.p-unprice> span') else None
        for item in soup.select(".info-technical > .tbl-technical  tr"):
            td = item.select("td")
            print(td)
            # Kiểm tra xem hàng có ít nhất 2 phần tử td không
            if len(td) >= 2:
                # Trích xuất văn bản từ thẻ span đầu tiên trong phần tử td đầu tiên và sử dụng strip() để loại bỏ các khoảng trắng thừa
                key = td[0].get_text().strip()
                value = td[1].get_text().strip()
                key = key.replace("\n", "").lower().strip()
                value = value.replace('\n',"")
                data[key] = value
        # for item in soup.select(".tbl-technical tr"):
        #     td = item.select("td")
        #     if len(td) > 1:
        #         key = td[0].get_text()
        #         value = td[1].get_text()

        #         key = key.replace("\n", "").lower().strip()
        #         value = value.replace('\n',"")
        #         data[key] = value
        data['url'] = link.replace("\n", "")
        return data

if __name__ == "__main__":
    crawler = PhilongCrawlData()
    crawler.exec()