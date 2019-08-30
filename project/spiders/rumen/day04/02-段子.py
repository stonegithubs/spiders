import re

import requests
from lxml import etree

url = 'https://www.neihanba.com/dz/list_43.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
while True:
    resp = requests.get(url, headers=headers)
    resp = resp.content.decode('gbk')
    resp1 = etree.HTML(resp)
    res = resp1.xpath('//ul/li/h4/a/b/text()')
    ret = resp1.xpath('//ul/li/div[@class="f18 mb20"]/text()')

    for i in range(len(res)):
        # print(res[i] + '\n' + ret[i] + '\n\n')
        with open('./files/neihanduanzi.txt','a')as f:
            f.write(ret[i] + '\n\n')
    # print(resp)
    url = re.findall(r'<a href="/dz/list_(\d+).html">下一页</a>', resp)
    print(url)
    if url:
        url = 'https://www.neihanba.com/dz/list_' + url[0] + '.html'
    else:
        break
