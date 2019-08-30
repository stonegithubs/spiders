import requests
import json


def run():
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Host': 'a.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB',
        'Cookie': '_ga=GA1.2.1887587483.1547955764; _gid=GA1.2.1722284729.1547955764; user_trace_token=20190120114244-7232e413-1c65-11e9-8157-525400f775ce; LGUID=20190120114244-7232e815-1c65-11e9-8157-525400f775ce; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22168695a7bcc12c3-0159ca18057785-162a1c0b-2073600-168695a7bcdb10%22%2C%22%24device_id%22%3A%22168695a7bcc12c3-0159ca18057785-162a1c0b-2073600-168695a7bcdb10%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3Dlagouwnag; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547955764,1547955776,1547955781; LGSID=20190120114301-7c89b2a7-1c65-11e9-8157-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fbeijing-zhaopin%2F%3Futm_source%3Dm_cf_cpt_baidu_pc1; _gat=1; LGRID=20190120120317-51629e86-1c68-11e9-819d-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547956998',

    }
    data = {
        'first': 'false',
        'pn': 3,
        'kd': 'python爬虫'
    }
    resp = requests.post(url, headers=headers, data=data)
    # with open('./lagou.html', 'w')as f:
    #     f.write(resp.content.decode())
    print(resp)


if __name__ == '__main__':
    run()
