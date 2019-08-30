import re

import requests
from lxml import etree

url = 'https://www.guazi.com/zz/wuling'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': 'antipas=zS517d235277w7814617jT0X9094; uuid=68e4f4a4-e0b2-4f11-e9e0-6001ddf08108; clueSourceCode=%2A%2300; ganji_uuid=9721455318083463819383; sessionid=4b64f3bc-3c13-46ee-cb19-4872e49fde13; lg=1; cainfo=%7B%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2268e4f4a4-e0b2-4f11-e9e0-6001ddf08108%22%2C%22sessionid%22%3A%224b64f3bc-3c13-46ee-cb19-4872e49fde13%22%7D; close_finance_popup=2018-11-08; cityDomain=zz; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1541639848; preTime=%7B%22last%22%3A1541640770%2C%22this%22%3A1541639843%2C%22pre%22%3A1541639843%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1541640770'
}

resp = requests.get(url=url, headers=headers)
# print(resp.content.decode())

# '//ul//h2/text()'  # 标题
# '//ul//div[@class="t-i"]/text()'  # 年份公里
# '//ul//em[@class="line-through"]/text()'  # 价格
# '//ul//div[@class="t-price"]/em[@class="line-through"]/text()'  # 原价

response = resp.content.decode()
resp = etree.HTML(response)
car_title = resp.xpath('//ul//h2/text()')  # 标题
car_price = resp.xpath('//ul//div[@class="t-price"]/p/text()')  # 价格
car_year = re.findall('<div class="t-i">(.*?)<span class="icon-pad">', response)  # 年份
car_mileage = re.findall('</span>(.*?)</div>', response)  # 公里

# for i in range(len(car_title)):
#     print(car_title[i] + '\t' + car_year[i] + '\t' + car_mileage[i] + '\t' + car_price[i] + '万')


# 原价
# car_original_price = re.findall(r'<em class="line-through">(.*?)</em>', response)  # 原价
# print(len(car_original_price))
# for i in range(len(car_original_price)):
#     print(car_original_price[i])

car_original_price = resp.xpath('//ul//div[@class="t-price"]/em[@class="line-through"]/text()')  # 价格
for i in range(len(car_original_price)):
    print(car_original_price[i])
    if car_original_price[i]:
        print(1)
    else:
        print(0)
# car_yearq = re.findall('<em class="line-through">(.*?)</em>', response)  # 年份
# print(car_yearq)
