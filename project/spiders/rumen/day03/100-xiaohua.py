import requests
import os
import re

page = 0
while True:
    url = 'http://www.xiaohuar.com/list-1-{}.html'.format(page)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    resp = requests.get(url=url, headers=headers)
    content = resp.content.decode('gbk')
    page += 1
    if content != None:
        girl = re.findall('.*?<img width="210"  alt="(.*?)" src="(.*?)" />.*?', content)
        for i in range(len(girl)):
            src = girl[i][1]
            image = 'https:'
            if image not in src:
                src = 'http://www.xiaohuar.com/' + src
            path = "./image/%s-%s" % (page, i + 1)
            path = path + girl[i][0] + '.jpg'
            print(src)
            if not os.path.exists(path):
                r = requests.get(src)
                with open(path, 'wb')as f:
                    f.write(r.content)
                print('图片保存成功')
            else:
                print('图片已存在')
    else:
        break
