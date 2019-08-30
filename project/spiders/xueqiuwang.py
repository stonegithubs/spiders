import requests
import json

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'aliyungf_tc=AQAAAMQ8bCgNDwYAPWmIdWsS1chYFHW3; xq_a_token=08f4dfd2f3103859dd6f4f2e95316bc748da319e; xq_a_token.sig=xs70B1ZJCaxRbNgDJ-FcCQ7VohU; xq_r_token=31d8d0b268493292213c26e5adbc7bb3961a208d; xq_r_token.sig=C0zjq4T5qJlcnH1_0wXW6kBAYX0; _ga=GA1.2.1082763529.1558531126; _gid=GA1.2.1180230758.1558531126; _gat=1; u=361558531126004; Hm_lvt_1db88642e346389874251b5a1eded6e3=1558531126; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1558531126; device_id=9275ca386069c10464d0c07e54908949',
    'Host': 'xueqiu.com',
    'Referer': 'https://xueqiu.com/u/cfbond',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=1&user_id=1759432827'

res = requests.get(url=url, headers=headers)
res = res.content.decode()
res = json.loads(res)
print(res)
for i in res['statuses']:
    print(i['title'])
    print(i['text'])
