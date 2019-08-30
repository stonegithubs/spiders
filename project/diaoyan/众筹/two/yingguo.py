import re

import requests
from lxml import etree


def yingguo(i):
    url = 'https://gogetfunding.com/wp-content/themes/ggf/fpage/fajx.php'

    data = {
        'step': 'get_more_blog_msg_commnets',
        'page': i,
        'lang': 'en',
        'pre': '6173916'
    }
    try:
        res = requests.post(url, data).text
    except:
        res = ''
        print('请求失败')
        yingguo(i)
    res = etree.HTML(res)
    try:
        name = res.xpath('//div/p/span/text()|//div/p/a/text()')
        jine = res.xpath('//div//p[@class="brokersText-20"]/text()')
        print(name)
    except:
        name = ''
        jine = ''
        print('xpath失败')
        yingguo(i)
    print(jine)
    for j, k in enumerate(jine):
        if 'Anonymous' in name[j]:
            continue
        else:
            jine = re.findall(r"[$][0-9\.]+", k, re.DOTALL)
            try:
                jine = jine[0]
            except:
                jine = 'Amount Hidden'
        p = re.findall("[A-Za-z]+\s[0-9]{1,2},\s[0-9]{4}", k, re.DOTALL)
        print(name[j])
        # print(jine)
        # print(p[0])
        with open('data.txt', 'a+', encoding='utf8')as f:
            f.write('xiang gang ji zhe xie hui bao hu ji zhe ji jin' + '^' + 'HK$3257818' + '^' + name[
                j] + '^' + jine + '^' + p[0] + '\n')
        # t = re.findall(r"[$][0-9\.]+", jine[j], re.DOTALL)
        # print(t)
        # p = re.findall("[A-Za-z]+\s[0-9]{1,2},\s[0-9]{4}", jine[j], re.DOTALL)
        # print(p)
        # with open('data.txt','a+',encoding='utf8')as f:
        #     f.write(name[j]+'^'+jine[j]+'\n')
        # break


if __name__ == '__main__':
    for i in range(1002, 10000):
        print('第' + str(i) + '页')
        yingguo(i)
