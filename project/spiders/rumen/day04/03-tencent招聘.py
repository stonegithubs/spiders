import re

import requests
from lxml import etree

url = 'https://hr.tencent.com/position.php?keywords=请输入关键词'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
resp = requests.get(url, headers=headers)
resp = resp.content.decode()
# resp = etree.HTML(resp)
print(resp)
# btetle = resp.xpath('((//tbody/tr[@class="even"]/td/a) | (//tbody/tr[@class="odd"]/td/a))/text()')
# print(btetle)
# for i in btetle:
#     print(btetle)
# print(resp)
# resp = re.findall(
#     r'<td class="l square"><a target="_blank" href="position_detail.php?id=45455&keywords=&tid=0&lid=0">(.*?)</a></td>',
#     resp)
# print(resp)
#
with open('./files/tencent-招聘1.html', 'w')as f:
    f.write(resp)
    # print(resp)
#     resp = re.findall(
#         r'<td class="l square"><a target="_blank" href="position_detail.php?id=45455&keywords=&tid=0&lid=0">(.*?)</a></td>',
#         resp)
#     print(resp)
