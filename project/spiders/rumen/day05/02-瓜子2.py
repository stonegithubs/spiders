import re
from pprint import pprint

import requests
from lxml import etree

url = 'https://www.guazi.com/zz/wuling'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': 'antipas=zS517d235277w7814617jT0X9094; uuid=68e4f4a4-e0b2-4f11-e9e0-6001ddf08108; clueSourceCode=%2A%2300; ganji_uuid=9721455318083463819383; sessionid=4b64f3bc-3c13-46ee-cb19-4872e49fde13; lg=1; cainfo=%7B%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2268e4f4a4-e0b2-4f11-e9e0-6001ddf08108%22%2C%22sessionid%22%3A%224b64f3bc-3c13-46ee-cb19-4872e49fde13%22%7D; close_finance_popup=2018-11-08; cityDomain=zz; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1541639848; preTime=%7B%22last%22%3A1541640770%2C%22this%22%3A1541639843%2C%22pre%22%3A1541639843%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1541640770'
}
all_data = []
response = requests.get(url, headers=headers)
resp = response.content.decode()
resp = etree.HTML(resp)
res = resp.xpath('//li[@data-scroll-track]/a')
x = 1
for i in res:
    data = {}
    data['ctitle'] = i.xpath('./h2/text()')[0]
    data['cyear'] = i.xpath('./div[@class="t-i"]/text()')[0]
    data['km'] = i.xpath('./div[@class="t-i"]/text()')[1]
    data['price'] = i.xpath('./div[@class="t-price"]/p/text()')[0]
    data['image'] = i.xpath('./img/@src')[0]
    original_price = i.xpath('./div/em/text()')
    if original_price:
        data['original_price'] = original_price[0]
    else:
        data['original_price'] = '暂无报价'
    # print(data['ctitle'] + '\t' + data['cyear'] + '\t' + data['km'] + '\t' + data['price']+'\t'+data['original_price'])
    # print(data['image'])
    all_data.append(data)
    ret = requests.get(data['image'])
    rew = re.findall(r'https://image.*.guazistatic.com/(.*?).jpg', data['image'])
    ret = ret.content
    req = rew[0]
    print(data['image'])

    with open('./images/{}.jpg'.format(x), 'wb')as f:
        f.write(ret)
        x += 1
