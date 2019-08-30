import requests
from lxml import etree


class HaiKangSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'UM_distinctid=16c3c917fa3216-076edf2dc18134-3f385c06-100200-16c3c917fa4742; CNZZDATA1262633151=956786054-1564384107-https%253A%252F%252Fwww.hikvision.com%252F%7C1564384107; FrontEnd.TenantId=8df2d413-6a5b-4c5f-8596-9f56c8b5080b; FrontEnd.CultureName=en; ASP.NET_SessionId=tub0k04y3qxdwlk01v30rofg',
            'Host': 'www.hikvision.com',
            # 'If-Modified-Since': 'Fri, 19 Jul 2019 09:28:36 GMT',
            # 'If-None-Match': '"da7f8457143ed51:0"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers).content.decode('utf8')
        # res = res.encoding('utf8')
        return res



    def run(self, url):
        res = self.get_html(url)
        res = etree.HTML(res)
        internet = res.xpath('/html/body/div[5]/div/div[1]/div/a/@href')[:3]
        internet.append(res.xpath('/html/body/div[5]/div/div[1]/div[21]/a/@href')[0])
        for i in internet:
            detail_list = self.get_html('https://www.hikvision.com/cn/' + i)
            detail_list = etree.HTML(detail_list)
            detail_url=detail_list.xpath('/html/body/div[5]/div/div[1]/ul/li//a/@href')[1:]
            for j in detail_url:
                detail_data = self.get_html('https://www.hikvision.com/cn/'+j)
                detail_data=etree.HTML(detail_data)
                data_list = detail_data.xpath('//div[@class="pagelist1 clearfix"]/div/div[2]/a/@href')
                # print(len(data_list))
                for k in data_list:
                    if len(k)!=0:
                        # print(k)
                        data = self.get_html('https://www.hikvision.com/cn/'+str(k))
                        # print(data)
                        data=etree.HTML(data)
                        # title = data.xpath('/html/body/div[5]/div[2]/div[2]/div[2]/div[2]/div[2]/text()')
                        try:
                            title = data.xpath('//div[@class="prdo6"]//text()')[0]
                        except:
                            continue
                        content = data.xpath('//div[@class="prgs"]//text()')
                        if title:
                            print('https://www.hikvision.com/cn/'+str(k))
                            print(title)
                            # print(content)
                            text = ''
                            for j in content:
                                text+=j.strip()
                            # print(text)
                            with open('./haikang.txt','a+',encoding='utf8')as f:
                                f.write(title+'^'+text+'\n')

if __name__ == '__main__':
    url = 'https://www.hikvision.com/cn/prlb_1608.html'
    tu = HaiKangSpider()
    tu.run(url)
    # a = 'a\r\nb\rc'
    # print(a.split())