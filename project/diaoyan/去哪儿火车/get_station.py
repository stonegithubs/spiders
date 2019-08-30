import re

import requests

def Get_Station():
    url = 'https://www.12306.cn/index/script/core/common/qss_v10036.js'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'BIGipServerpool_index=837812746.43286.0000; RAIL_EXPIRATION=1565523969445; RAIL_DEVICEID=q2gAkoxQunPnhS6hjV5mMI0i5o6LqdzlnNWLFPe-gvGMYyHJSRHGMC0ns4n42FjqAIb2MmfHdPx4K3LH0yEqjAE9ybJyTCT0k4D4RhmVK1c34pRTGqXOiCAAq3IBAKs3I7E3V4SQa7gSSoD1M1rsqt12jBy7bsb1; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=1156579850.50210.0000',
        'Host': 'www.12306.cn',
        'If-Modified-Since': 'Wed, 07 Aug 2019 07:18:51 GMT',
        'If-None-Match': '"5d4a7b5b-e1b3"',
        'Referer': 'https://www.12306.cn/index/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    res = requests.get(url,headers).text
    res = res.split(',')
    # print(res)
    a = []
    for i in res:
        city = re.findall(r'"(.*?)"',i)
        # if city[0]:
        #     print(a)
        with open('./station_info.txt','a',encoding='utf8')as f:
            f.write(city[0]+'\n')
        a.append(city[0])
    return a


if __name__ == '__main__':
    a = Get_Station()
    print(a)
    print(len(a))