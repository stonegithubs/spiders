import requests
from lxml import etree
import re


def top500spider():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
        'Cache-Control': 'max-age=0',
        'Cookie': 'BAIDU_SSP_lcr=https://www.baidu.com/link?url=LL3jvgHKLusqCyy0JCj5CqpBxZdWtP4bwFceayhZVj86wD3dX3yiPOKYvyVkJvJ_7rbnwfmDFS235ejEthGBvaTbh7VoKxXoxXFrBShdy13&wd=&eqid=cae9e21e000581b0000000035d2841e0; aliyungf_tc=AQAAAHVUln6SNgQAXg4gLfpkTET7mDHs; acw_tc=0bc1a05415629193992807931ec0dee4dd5442f1447b7d62b209a7e4e92928; _ga=GA1.2.1244223913.1562919413; _gid=GA1.2.207091292.1562919413; _gat=1',
        'Host': 'www.fortunechina.com',
        'If-Modified-Since': 'Thu, 11 Jul 2019 15:43:44 GMT',
        'If-None-Match': 'W/"5d275930-1dceb"',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    url = 'http://www.fortunechina.com/fortune500/c/2019-07/10/content_337536.htm'
    res = requests.get(url,headers)
    res = res.content.decode()
    # with open('top.html', 'w', encoding='utf-8')as f:
    #     f.write(res)
    # res = etree.HTML(res)
    # name = res.xpath('//div[@id="yytable_wrapper"]//tr//a/text()')
    name = re.findall(r'target="_blank">(.*?)</a> </td><td>',res)
    print(name)
    print(len(name))


if __name__ == '__main__':
    top500spider()
