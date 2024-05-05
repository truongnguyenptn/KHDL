from selenium import webdriver
import csv
import atexit
from Config import Config

class CrawlData:
    DOMAIN = ""
    DETAIL_LINK_FILE = ""
    RAW_DATA_FILE = ""
    driver = webdriver.Chrome()

    def _save_detail_link_file(self, link_details):
        with open(self.DETAIL_LINK_FILE, "w", encoding="utf-8") as f:
            for link in link_details:
                f.write(link + "\n")

    def _read_detail_link_file(self):
        link_details = None
        with open(self.DETAIL_LINK_FILE, "r") as f:
            link_details = f.readlines()
        return link_details
    
    def exec(self, ignore_get_detail_link=False):
        if ignore_get_detail_link == False:
            link_details = self.get_detail_links()
            self._save_detail_link_file(link_details)

        with open(self.RAW_DATA_FILE, "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator='\n')
            header, header_set = [], set()

            @atexit.register 
            def printHeader(): 
                print(">>> ")
                print(header)
            
            link_details = self._read_detail_link_file()
            for link in link_details:
                try:
                    info = self.get_info(link)
                except Exception as e:
                    print("=============")
                    print(info)
                    print(link)
                    print(str(e))
                    print("====><=====")
                    continue
                
                for key in info.keys():
                    if key not in header_set:
                        key = key.replace("\n", "")
                        header_set.add(key)
                        header.append(key)
                writer.writerow(info.get(col, '') for col in header)
            
            f.seek(0)
            f.writelines(",".join(header))

            print(",".join(header))
    
    def get_detail_links(self):
        '''
            Duyệt qua tất cả trang sản phẩm để lấy tất cả đường link chi tiết sản phẩm

            Output: List[string] Danh sách các đường link chi tiết sản phẩm
        '''
        pass

    def get_info(self, link):
        '''
            Phân tích trang sản phẩm chi tiết để lấy các dữ liệu cần thiết
            
            Input: URL chi tiết sản phẩm
            Output: Dict[str, str] chứa dữ liệu trích xuất từ HTML
        '''
        pass
