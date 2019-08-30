import requests
import execjs
import re
import json


def baidu_fanyi():
    query = input(">")
    url = "https://fanyi.baidu.com/v2transapi"
    sign, token = get_data(query)
    lang = get_lang(query)

    if lang == "zh":
        data = {
            "from": "zh",
            "to": "en",
            "query": query,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
        }
    else:
        data = {
            "from": "en",
            "to": "zh",
            "query": query,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
        }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "136",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "BAIDUID=A0CB0FE1DB6D18809C712B5062BBAC6F:FG=1; BIDUPSID=A0CB0FE1DB6D18809C712B5062BBAC6F; PSTM=1538210057; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1539151103,1539251833; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; from_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; delPer=0; H_PS_PSSID=1438_21082_27401_26350; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541035594,1541036302,1541037057,1541040002; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541040002; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=5; ZD_ENTRY=baidu; pgv_pvi=4554512384; pgv_si=s8051585024",
        "Host": "fanyi.baidu.com",
        "Origin": "https://fanyi.baidu.com",
        "Referer": "https://fanyi.baidu.com/translate?aldtype=16047&query=%E7%BE%8E%E5%A5%B3%0D%0A&keyfrom=baidu&smartresult=dict&lang=auto2zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    proxies = {
        "https": "https://202.112.237.102:3128"
    }
    resp = requests.post(url=url, data=data, headers=headers, proxies=proxies)

    content = resp.content.decode("utf-8")
    content = json.loads(content)
    print(content["trans_result"]["data"][0]["dst"])


def get_data(query):
    url = "https://fanyi.baidu.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Cookie": "BAIDUID=A0CB0FE1DB6D18809C712B5062BBAC6F:FG=1; BIDUPSID=A0CB0FE1DB6D18809C712B5062BBAC6F; PSTM=1538210057; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1539151103,1539251833; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; pgv_pvi=4554512384; delPer=0; H_PS_PSSID=1438_21082_27401_26350; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541036302,1541037057,1541040002,1541054643; PSINO=5; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541057937; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D"
    }

    resp = requests.get(url=url, headers=headers)
    content = resp.content.decode("utf-8")

    gtk = re.findall(r"<script>window.bdstoken = '';window.gtk = '(.*?)';</script>", content)[0]
    token = re.findall(r"token: '(.*?)',", content)[0]

    print(gtk)
    print(token)

    with open("./files/fanyi.js", "r", encoding="utf-8") as file:
        js = file.read()

    js = js.replace('u = null !== i ? i : (i = window[l] || "") || "";', 'u = "%s"' % gtk)

    cxt = execjs.compile(js)

    sign = cxt.call("e", query)
    print(query, sign)
    return sign, token


def get_lang(query):
    url = "https://fanyi.baidu.com/langdetect"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Cookie": "BAIDUID=A0CB0FE1DB6D18809C712B5062BBAC6F:FG=1; BIDUPSID=A0CB0FE1DB6D18809C712B5062BBAC6F; PSTM=1538210057; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1539151103,1539251833; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; pgv_pvi=4554512384; delPer=0; H_PS_PSSID=1438_21082_27401_26350; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541036302,1541037057,1541040002,1541054643; PSINO=5; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541057937; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D"
    }
    data = {
        "query": query
    }
    resp = requests.post(url=url, data=data, headers=headers)
    content = resp.content.decode("utf-8")
    content = json.loads(content)
    print(content["lan"])
    return content["lan"]


if __name__ == '__main__':
    baidu_fanyi()

"""
反爬：
    1、useragent
    2、cookie
    3、ip
    4、js生成的数据
    
反反爬
    1、加上正确的useragent，多找几个，随机获取一个
    2、查看浏览器，获取真实cookie
    3、使用代理ip,建议购买高效稳定高匿
    4、分析搜索，可以借助pyexecjs+node.js等api运行js代码
"""

def fanyi1():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', }
    lang = get_lang(query_string)
    if lang == 'zh':
        post_data = {
            'query': query_string,
            'from': 'zh',
            'to': 'en',
        }
    else:
        post_data = {
            'query': query_string,
            'from': 'en',
            'to': 'zh',
        }

    post_url = 'https://fanyi.baidu.com/basetrans'
    r = requests.post(url=post_url, data=post_data, headers=headers)
    dict_ret = json.loads(r.content.decode())
    ret = dict_ret['trans'][0]['dst']
    print(query_string + ':' + ret)


def get_lang1(query):
    url = "https://fanyi.baidu.com/basetrans"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
        'Cookie': 'BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=A925DA33619800BC358633490918CA1B; PSTM=1540984814; BAIDUID=DEDCBAE80EADD0EEC573F5529900E7D8:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; delPer=0; H_PS_PSSID=1442_21117_27400_26350; PSINO=5; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1541059955,1541062371,1541064619,1541081327; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1541081327; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541071518,1541071569,1541081310,1541081327; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541081327',
    }
    data = {
        "query": query
    }
    resp = requests.post(url=url, data=data, headers=headers)
    content = resp.content.decode("utf-8")
    content = json.loads(content)
    print(content)
    print(content["lan"])
    return content["lan"]
