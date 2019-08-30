import re
import requests
from lxml import etree

url = 'https://www.neihan8.com/wenzi//'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

resp = requests.get(url, headers=headers)
resp = resp.content.decode()

resp = etree.HTML(resp)
res = resp.xpath('//div[@class="text-column-item box box-790"]/h3/a/text()')
ret = resp.xpath('//div[@class="text-column-item box box-790"]/div[@class="desc"]/text()')

for i in range(len(res)):
    # print(res[i] + '\n' + ret[i] + '\n\n')
    with open('./files/duanzi.txt','a')as f:
        f.write(res[i] + '\n' + ret[i] + '\n\n')
