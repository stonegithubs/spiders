import requests

url = 'https://api.pinduoduo.com/api/jinbao/wechat/goods/query_goodslist?pdduid=0&__json=1'
data = {
    'hasCoupon': 0,
    'keyword': "手机",
    'merchantTypeList': 'null',
    'pageNum': 1,
    'pageSize': 20,
    'rangeItems': 'null',
    'sortType': 1,
}
headers = {
    # 'Content-Type': 'text/plain;charset=UTF-8',
    # 'Origin': 'https://mobile.yangkeduo.com',
    # 'Referer': 'https://mobile.yangkeduo.com/duo_cms_result.html?pid=1_72219131&cpsSign=CM_190611_1_72219131_9d3e0f32662c65c11d9e79f7d86ac93c&authDuoId=0&duoduo_type=2&search_key=%E6%89%8B%E6%9C%BA&refer_page_name=duo_cms_mall&refer_page_id=10598_1563930172357_68RI9cWlzX&refer_page_sn=10598',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}
res = requests.post(url=url,headers=headers, data=dict(data))
print(res)
