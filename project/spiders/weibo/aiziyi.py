import requests
import json
import re

import xlwt

url = 'https://m.weibo.cn/api/container/getIndex?uid=5781311106&luicode=10000011&lfid=100103type%3D3%26q%3D%E6%95%96%E5%AD%90%E9%80%B8%26t%3D0&type=uid&value=5781311106&containerid=1076035781311106&page={}'
res = []
for i in range(1, 28):
    resp = requests.get(url.format(i))
    content = json.loads(resp.content.decode())
    contents = content['data']['cards']
    for content in contents:
        data = {}
        if 'mblog' in content:
            data['created_time'] = content['mblog']['created_at']
            data['message'] = content['mblog']['text']
            # print(created_time, message)
            data['message'] = re.sub(r'<.*?>', '', data['message']) 
            # with open('aoziyi.txt', 'a')as f:
            #     f.write('时间：' + created_time+'\t' + '内容：' + message + '\n')
            # print(data)
            res.append(data)
print(res)

from pandas import DataFrame as DF
df = DF(res)
df.to_csv('aoziyi.csv')




# s1 = '<a>1</a>23'
# s2 = re.sub(r'<.*?>','',s1)
# print(s2)
