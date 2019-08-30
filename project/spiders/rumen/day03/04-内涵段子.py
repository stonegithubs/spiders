import requests
import json
import re


def f1():
    url = 'https://www.neihanba.com/dz/'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    with open('../files/duanzi.txt', 'w')as f:
        f.write('')
    while True:
        response = requests.get(url=url, headers=headers)
        resp = response.content.decode('gbk')

        res = re.findall(r'<h4> <a href="/dz/\d+.html"><b>(.*?)</b></a></h4>', resp)
        ret = re.findall(r'<div class="f18 mb20">(.*?)</div>', resp)

        for i in range(len(res)):
            # print(res[i] + '\n' + ret[i])
            with open('../files/duanzi.txt', 'a')as f:
                f.write(res[i] + '\n' + ret[i] + '\n')

        url = re.findall(r'<a href="/dz/list_(\d+).html">下一页</a>', resp)

        print(url)
        if url:
            url = 'https://www.neihanba.com/dz/list_' + url[0] + '.html'
        else:
            break


if __name__ == '__main__':
    f1()
