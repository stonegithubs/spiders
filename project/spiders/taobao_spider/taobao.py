"""import requests

start_url = 'https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1546944266575_1129&callback=jsonp1130&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190108&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44'

# proxies = {
#     'https': '183.148.139.249:9999'
# }
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
data = {
    'cookie': 'miid=109533513542190173; t=c99f5a4789e1d5abfb1dedd25c310ddb; thw=cn; cna=MT2NFHB7+kECAXrAJrPBsmFA; v=0; cookie2=33a0870151d678d471cb71ab962aa08b; _tb_token_=34b8b0d388da9; unb=3454914747; sg=87e; _l_g_=Ug%3D%3D; skt=69eeb0908f92b088; cookie1=UUo3uo3wQOs3ax2200WO%2FkaRsV%2F6FWq%2FYjCEGHtVASU%3D; csg=d5f71136; uc3=vt3=F8dByEzfipmxb7pxFKw%3D&id2=UNQyRovnY7he0w%3D%3D&nk2=F5RFhSMP1VMEtr0%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTU1MDU3OTM3Mg%3D%3D; tracknick=tb058147578; lgc=tb058147578; _cc_=Vq8l%2BKCLiw%3D%3D; dnk=tb058147578; _nk_=tb058147578; cookie17=UNQyRovnY7he0w%3D%3D; tg=5; mt=ci=0_1; enc=RuAki8VTD8%2Fzr6vk3NO1iE8LSWA7pepOvqeZifVdGVoDILqvjEgodQZAPwR4A%2BgNN4AxPkoN%2BFCZcImGXLM4jA%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; uc1="cookie15=VT5L2FSpMGV7TQ%3D%3D"; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=53928; JSESSIONID=155101989FB7566AB42EB50038019DDF; isg=BLCw7u1fmNiRNUSIqVjTBoiQgXfCUZ_u66y_bqoBdIveZVAPUgqA0wZUuS2gPUwb; l=bBr01uFPvHVgRpFZBOCNiuIRfwQtSIRvMuPRwlfWi_5Q46L_gNQOllXLPFp6Vj5R_X8B4mebW5J9-etew; x5sec=7b227365617263686170703b32223a22306435393338323837353262383335623731633463613937303430623134666643497679722b4d46454b6172694b713430496d7a6f67456144444d304e5451354d5451334e4463374d773d3d227d',
}
# resp = requests.post(start_url, proxies=proxies)
resp = requests.post(url=start_url, headers=headers, data=data)
# print(resp.status_code)
with open('taobao.html', 'w')as f:
    f.write(resp.text)


import requests
import re


'''
目标：获取淘宝搜索页面的信息，提取其中的商品名称和价格
理解： 淘宝的搜索接口 翻页的处理
技术路线：requests‐bs4‐re
'''


# 步骤1：提交商品搜索请求，循环获取页面
def get_html_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    proxies = {
        'https': '112.85.164.159:9999'
    }
    try:
        coo = 't=85db5e7cb0133f23f29f98c7d6955615; cna=3uklFEhvXUoCAd9H6ovaVLTG; isg=BM3NGT0Oqmp6Mg4qfcGPnvDY3-pNqzF2joji8w9SGWTYBu241_taTS6UdFrF3Rk0; miid=983575671563913813; thw=cn; um=535523100CBE37C36EEFF761CFAC96BC4CD04CD48E6631C3112393F438E181DF6B34171FDA66B2C2CD43AD3E795C914C34A100CE538767508DAD6914FD9E61CE; _cc_=W5iHLLyFfA%3D%3D; tg=0; enc=oRI1V9aX5p%2BnPbULesXvnR%2BUwIh9CHIuErw0qljnmbKe0Ecu1Gxwa4C4%2FzONeGVH9StU4Isw64KTx9EHQEhI2g%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=0_0; hibext_instdsigdipv2=1; JSESSIONID=EC33B48CDDBA7F11577AA9FEB44F0DF3'
        cookies = {}
        for line in coo.split(';'):  # 浏览器伪装
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        r = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 步骤2：对于每个页面，提取商品名称和价格信息
def parse_page(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)  # findall搜索全部字符串，viex_price是源代码中表价格的值，后面的字符串为数字和点组成的字符串
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)  # 找到该字符串和后面符合正则表达式的字符串
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])  # re.split() 将一个字符串按照正则表达式匹配结果进行分割，返回列表类型
            title = eval(tlt[i].split(':')[1])  # 将re获得的字符串以：为界限分为两个字符串,并取第二个字符串
            ilt.append([price, title])
    except:
        print('')


# 步骤3：将信息输出到屏幕上
def print_goods_list(ilt):
    tplt = "{:4}\t{:8}\t{:16}"  # 长度为多少
    print(tplt.format('序号', '价格', '名称'))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))


def main():
    # goods = '铅笔'
    depth = 1 # 要爬取几页
    start_url = 'https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1546944266575_1129&callback=jsonp1130&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190108&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44'
    info_list = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)  # 44是淘宝每个页面呈现的宝贝数量
            html = get_html_text(url)
            parse_page(info_list, html)
        except:
            continue
    print_goods_list(info_list)


main()


import urllib.request
import urllib.parse
import http.cookiejar

url = "https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1546944266575_1129&callback=jsonp1130&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190108&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44"
postdata = urllib.parse.urlencode({
    "username": "weisuen",
    "password": "aA123456"
}).encode('utf-8')
req = urllib.request.Request(url, postdata)
req.add_header('User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
# 使用http.cookiejar.CookieJar()创建CookieJar对象
cjar = http.cookiejar.CookieJar()
# 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
# 将opener安装为全局
urllib.request.install_opener(opener)
file = opener.open(req)
data = file.read()
file = open("3.html", "wb")
file.write(data)
file.close()
url2 = "http:// bbs.chinaunix.net/"
data2 = urllib.request.urlopen(url2).read()
fhandle = open("4.html", "wb")
fhandle.write(data2)
fhandle.close()
"""
# -*- coding: utf-8 -*-
import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
import matplotlib
# 计时开始
start = time.clock()
# plist 为1-100页的URL的编号num
plist = []
for i in range(1, 101):
    j = 44 * (i-1)
    plist.append(j)

listno = plist
datatmsp = pd.DataFrame(columns=[])

while True:
    # 设置最大重试次数
    @retry(stop_max_attempt_number = 8)
    def network_programming(num):
        url = 'https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1546944266575_1129&callback=jsonp1130&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190108&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=' + str(num)
        web = requests.get(url, headers=headers)
        web.encoding = 'utf-8'
        return web

    # 多线程
    def multithreading():
        # 每次爬取未爬取成功的页
        number = listno
        event = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(network_programming, number, chunksize=10):
                event.append(result)

        return event

    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

    }

    listpg = []
    event = multithreading()
    for i in event:
        json = re.findall(
        '"auctions":(.*?),"recommendAuctions"', i.text)
        if len(json):
            table = pd.read_json(json[0])
            datatmsp = pd.concat([datatmsp, table],
                                axis=0, ignore_index=True)

            pg = re.findall(
            '"pageNum":(.*?),"p4pbottom_up"', i.text)[0]
            listpg.append(pg)

    lists = []
    for a in listpg:
        b = 44 * (int(a)-1)
        lists.append(b)

    listn = listno

    listno = []
    for p in listn:
        if p not in lists:
            listno.append(p)

    if len(listno) == 0:
        break

datatmsp.to_excel('./data/datastmsp.xls', index=False)

end = time.clock()
print("爬取完成，用时: ",end-start, 's')
