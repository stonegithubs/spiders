import json

import pymysql
import requests

url = 'https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?for_mobile=1&start=0&count=18&loc_id=108288'
headers = {
    'Referer': 'https://m.douban.com/movie/nowintheater?loc_id=108288',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}
response = requests.get(url=url, headers=headers)
# print(response.status_code)
resp = response.content.decode()
resp = json.loads(resp)
res = resp['subject_collection_items']
# print(resp)

# print(len(resp['subject_collection_items']))

for i in range(len(resp['subject_collection_items'])):
    res = resp['subject_collection_items'][i]['title']
    ref = resp['subject_collection_items'][i]['url']
    # print(resp['subject_collection_items'][i]['rating'])

    if resp['subject_collection_items'][i]['rating']:
        ret = resp['subject_collection_items'][i]['rating']['value']
    else:
        ret = ''
    # print(res + '\t' + str(ret) + '\t' + ref)
    # conn = pymysql.connect(host='192.168.12.135', port=3306, db='movie', user='root', password='.', charset='utf-8')
    conn = pymysql.connect(user="root", password=".", port=3306, db="movie", host="192.168.12.135", charset="utf8")  # 创建数据库连接
    c1 = conn.cursor()
    sql = """insert into movie(mname,mscore,mlink) values(%s,%s,%s)"""
    # for i in range(len(resp['subject_collection_items'])):
    c1.execute(sql, (res, str(ret), ref))
    conn.commit()
    conn.close()

# with open('../files/douban.json','w')as f:
#     f.write(resp)
