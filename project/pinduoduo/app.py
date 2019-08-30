import json

import requests


class PinduoduoAPPSpider(object):
    def __init__(self):
        self.key_word = '篮球'
        self.url = 'https://api.pinduoduo.com/api/jinbao/wechat/goods/query_goodslist?pdduid=0&__json=1'
        self.headres = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://mobile.yangkeduo.com',
            'Referer': 'https://mobile.yangkeduo.com/duo_cms_result.html?search_key={}'.format(self.key_word),
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }

    def run(self):
        post_data = {
            'hasCoupon': 0,
            'keyword': self.key_word,
            'merchantTypeList': 'null',
            'pageNum': 0,
            'pageSize': 20,
            'rangeItems': 'null',
            'sortType': 1
        }
        post_data = json.dumps(post_data)
        res = requests.post(url=self.url, headers=self.headres, data=post_data)
        # change = res.json()
        # new_res = json.dumps(change, ensure_ascii=False)
        # new_res = json.loads(new_res)
        print(res)


class PinSpider(object):
    def __init__(self):
        self.url = 'https://mobile.yangkeduo.com/proxy/api/search?source=search&search_met=manual&track_data=refer_page_id,10015_1563851573445_S6aCxFmlm5&list_id=qfeegYQnor&sort=default&filter=&q=%E7%AF%AE%E7%90%83&page=5&size=50&flip=80;4;0;60;cd309741-a75d-4c2e-86c5-3138cd0273ee&anti_content=0anAfxnUvyhYq9dVFj64w0r2_T5Yk1p_-G6mencZF2vLdXksel3HzJ8UAl3pE55OP-LWho2GhZV864fa4YeGvtbJrDh3RmrbaqfDC99J2_rVFOVCuDQei0Ss99G-FvNpBGo9jDpLJUariIgmWPZpKzYnyqQX5FesIESm1A_h2wfvXK11Exu-saNjgAe8PpnXLReQjRjqbbX0qm0jOK71ytgz1Li7MnKoO5S14Ktmb2sKcTZ48lcFyxy_5-veppMXaFKMHhoMNj6y7T_gSofZo5IYS9wbFQQENBSxoWIryqFL24cN9JBJ2vdZTzH5CdktR9zKhfnIaWJDc2wxI0hdhfiQ3RGX4g2A93pj9Ph97C6mJdrFytlKEHNyScsp8Hcg33UmZSosEGgJ9CcwBnpxbD7rCtcsRvqMRo4834w7JWsnFztlrqB1fyAfJzzKjVoWEOj6MYkPdPZ5s_k_ppUJZUE63QiWtLUMExhdcnYHzmp-okSW7vbXRqEjDg7d-psXWSHxxSOOgnPhz0JbxmuohIduNBPp8-eLOK22j31NMCiipfAbPs-H87OnRS-cIOWrUuiiW2JS7B365Rm0cLnStk7bIRK88IScKo&pdduid=0'
        self.headers = {
            'Referer': 'https://mobile.yangkeduo.com/search_result.html?search_key=%E7%AF%AE%E7%90%83&search_src=new&search_met=btn_sort&search_met_track=manual&refer_page_name=search_result&refer_page_id=10015_1563851573445_S6aCxFmlm5&refer_page_sn=10015',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'user-agent': 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        self.data = {
            'source': 'search',
            'search_met': 'manual',
            'track_data': 'refer_page_id,10015_1563851573445_S6aCxFmlm5',
            'list_id': 'qfeegYQnor',
            'sort': 'default',
            'filter': 'q: 篮球',
            'page': '5',
            'size': '50',
            'flip': '80;4;0;60;cd309741-a75d-4c2e-86c5-3138cd0273ee',
            'anti_content': '0anAfxnUvyhYq9dVFj64w0r2_T5Yk1p_-G6mencZF2vLdXksel3HzJ8UAl3pE55OP-LWho2GhZV864fa4YeGvtbJrDh3RmrbaqfDC99J2_rVFOVCuDQei0Ss99G-FvNpBGo9jDpLJUariIgmWPZpKzYnyqQX5FesIESm1A_h2wfvXK11Exu-saNjgAe8PpnXLReQjRjqbbX0qm0jOK71ytgz1Li7MnKoO5S14Ktmb2sKcTZ48lcFyxy_5-veppMXaFKMHhoMNj6y7T_gSofZo5IYS9wbFQQENBSxoWIryqFL24cN9JBJ2vdZTzH5CdktR9zKhfnIaWJDc2wxI0hdhfiQ3RGX4g2A93pj9Ph97C6mJdrFytlKEHNyScsp8Hcg33UmZSosEGgJ9CcwBnpxbD7rCtcsRvqMRo4834w7JWsnFztlrqB1fyAfJzzKjVoWEOj6MYkPdPZ5s_k_ppUJZUE63QiWtLUMExhdcnYHzmp-okSW7vbXRqEjDg7d-psXWSHxxSOOgnPhz0JbxmuohIduNBPp8-eLOK22j31NMCiipfAbPs-H87OnRS-cIOWrUuiiW2JS7B365Rm0cLnStk7bIRK88IScKo',
            'pdduid': '0',
        }

    def run(self):
        res = requests.get(self.url, self.headers)
        # with open('./duoduo.html','w',encoding='utf-8')as f:
        #     f.write(res)
        print(res)


if __name__ == '__main__':
    # pin = PinduoduoAPPSpider()
    pin = PinSpider()
    pin.run()
