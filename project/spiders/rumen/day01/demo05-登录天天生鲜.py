from pprint import pprint

import requests


def f1():
    url1 = 'http://www.renren.com/PLogin.do'
    url2 = 'http://www.renren.com/968561367/profile'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'anonymid=jo11a4dwdnlgno; depovince=HEN; _r01_=1; jebecookies=fb9a14dc-9cad-45a0-8ab4-b5d70860058d|||||; JSESSIONID=abcXxpQX3q3nU4S6zvyBw; ick_login=2850fcd8-ee5a-42d5-8de9-416d02f5916b; _de=0EA171ACA3C2F5B99DEC90D2B7E6F15B; p=fc51ad73bb5c552836c207a3a70201847; first_login_flag=1; ln_uact=18568453967; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=6897d1766363b1455361346500fe49507; societyguester=6897d1766363b1455361346500fe49507; id=968561367; xnsid=27a9f617; loginfrom=syshome; jebe_key=da3b5c7a-9cae-4a87-8f6d-0a3212d06740%7Cc057834d57cdb3967f50a944e4c10fe9%7C1541227814571%7C1%7C1541227817598; wp_fold=0', }
    data = {'email': '18568453967',
            'password': '0422.520dong'
            }
    session = requests.session()
    session.post(url=url1, data=data, headers=headers)
    r = session.get(url=url2, headers=headers)
    with open('./files/天天生鲜.html', 'w', encoding='utf-8') as file:
        file.write(r.content.decode())


"""人人账号
18568453967
0422.520dong
"""


def f2():
    url = 'http://www.renren.com/968561367/profile'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    cookies = 'anonymid=jo11a4dwdnlgno; depovince=HEN; _r01_=1; jebecookies=fb9a14dc-9cad-45a0-8ab4-b5d70860058d|||||; JSESSIONID=abcXxpQX3q3nU4S6zvyBw; ick_login=2850fcd8-ee5a-42d5-8de9-416d02f5916b; _de=0EA171ACA3C2F5B99DEC90D2B7E6F15B; p=fc51ad73bb5c552836c207a3a70201847; first_login_flag=1; ln_uact=18568453967; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=6897d1766363b1455361346500fe49507; societyguester=6897d1766363b1455361346500fe49507; id=968561367; xnsid=27a9f617; loginfrom=syshome; jebe_key=da3b5c7a-9cae-4a87-8f6d-0a3212d06740%7Cc057834d57cdb3967f50a944e4c10fe9%7C1541227814571%7C1%7C1541227817598; wp_fold=0'
    cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split('; ')}
    print(cookies)
    r = requests.get(url=url, headers=headers,cookies=cookies)

    with open('../files/renrne1.html', 'w', encoding='utf-8') as file:
        file.write(r.content.decode())


if __name__ == '__main__':
    # f1()
    f2()