import json
import re
import requests
from parse_url import parse_url
num = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
}
for i in range(5):
    url = 'http://www.xiaohuar.com/list-1-{}.html'.format(num)
    html_str = requests.get(url=url, headers=headers)

    print(num)

    ret = html_str.content.decode('gbk')
    # print(ret)

    res = re.findall('src="https://(.*?).jpg"', ret)
    for x in res:
        res = "https://' + x + '.jpg"

        r = requests.get(url=res,headers=headers)

        with open('./images/{}.jpg'.format(num), 'wb') as f:
            f.write(r.content)
    num = num + 1
    print(111)
