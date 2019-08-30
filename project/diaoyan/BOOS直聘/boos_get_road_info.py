import json
import time

import requests
from lxml import etree


class BoosGetCity(object):
    """类"""

    def __init__(self):
        """初始化"""
        self.base_url = 'https://www.zhipin.com'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'cookie': 'lastCity=101010100; _uab_collina=156706388077863819513474; __zp_stoken__=523emjHP%2Ff0b8XNQrhdF71%2BMQ5OCKqlh2dqR%2Fv030ej65DLEWSQJ62c4ahqCZ%2Be%2Fk2EebcGfnagCPvc3RvlLyRAuWQ%3D%3D; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1567063881,1567143802; __c=1567143802; __g=-; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%26city%3D101010100&r=&friend_source=0&friend_source=0; JSESSIONID=""; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1567145453; __a=98805445.1567063881.1567063881.1567143802.18.2.11.18'
        }

    def run(self):
        """主函数"""
        with open('citys_code.txt', 'r', encoding='utf8')as f:
            code = f.readlines()
            # print(code)
            a = 1
            for x in code:
                url = self.base_url+'/c'+x
                time.sleep(2)
                res = requests.get(url, headers=self.headers).text
                # print(res)
                elem = etree.HTML(res)
                detail_page_url = elem.xpath('//*[@id="filter-box"]/div/div[2]/dl[2]/dd/a/@href')
                # print(detail_page_url)
                # for i in detail_page_url[1:]:
                #     print(i)
                print(detail_page_url)
                a +=1
            print(a)

if __name__ == '__main__':
    boos = BoosGetCity()  # 创建对象
    boos.run()  # 调用函数
