import re

import requests


def f1():
    url = 'https://www.baidu.com/s?wd=中国'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        # 'Cookie': 'BIDUPSID = 381BF3AFAD0FC0C8E631D920FC97E9A9;BAIDUID = AC39374EBDFE0186290D3F268D30B32A:FG = 1;PSTM = 1540982875;delPer = 0;BD_HOME = 0;H_PS_PSSID = 1430_21092_26350_22074;BD_UPN = 123353;BD_CK_SAM = 1;PSINO = 5;BDORZ = B490B5EBF6F3CD402E515D22BCDA1598;H_PS_645EC = 311dy8rRibI5wwDTinoUNXFOjKBiBuQeFl9OwAoSuaYwuN4wZo8ijKUSUKs'
    }
    resp = requests.get(url=url, headers=headers)
    resp = resp.content

    with open('./files/baidu.html', 'wb') as file:
        file.write(resp)


def f2():
    num = 0
    res = 1
    name = input('请输入吧名:')
    for i in range(3):
        print('num:', num)
        url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(name, num)
        num = num + 50
        print('num:', num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }
        resp = requests.get(url=url, headers=headers)
        resp = resp.content

        with open('./files/tieba/{}-0{}.html'.format(name, res), 'wb') as file:
            file.write(resp)
        print('res:', res)
        res += 1
        print('res:', res)


def f3():
    """拼接url"""
    num = 1
    # name = input('请输入吧名:')
    kw = '捡垃圾'

    url = 'https://tieba.baidu.com/f?kw={}'.format(kw)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    }
    while True:
        # url = url.format(kw)

        resp = requests.get(url=url, headers=headers)
        resp = resp.content.decode()
        resp = resp.replace('<!--', '').replace('-->', '')  # 去掉网页注释

        with open('../files/tieba/{}-0{}.html'.format(kw, num), 'w') as file:
            file.write(resp)

        url = re.findall(r'<a href="(.*?)" class="next pagination-item', resp)
        print(url)

        if url:
            url = 'https:' + url[0]
        else:
            break

        print(num)
        num += 1


if __name__ == '__main__':
    # f1()
    # f2()
    f3()
