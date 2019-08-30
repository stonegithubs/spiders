import re
from parse_url import parse_url


with open('./douban.txt', 'w', encoding='utf8')as f:
    f.write('')

num = 0
for i in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(num)
    num = num + 25
    html_str = parse_url(url)
    with open('./douban.html', 'w', encoding='utf-8')as f:
        f.write(html_str)
    ret = re.findall('<span class="title">([^&nbsp;].*?)</span>', html_str)  # 电影名
    res = re.findall('导演:(.*)<br>', html_str)  # 导演名
    ref = re.findall('<span class="inq">(.*?)</span>', html_str)  # 简介
    # print(res)
    # print(ret)
    # print(ref)

    for x in range(len(ret)):

        with open('./douban.txt', 'a', encoding='utf8')as f:
            f.write('电影名:'+ret[x] + '\t' + '导演:' + res[x] + '\t\t' + '简介:' + ref[x] + '\n')
