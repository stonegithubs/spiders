import requests
from lxml import etree


class TuNiuSpider(object):
    def __init__(self):
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers).text
        return res

    def run(self, url):
        res = self.get_html(url)
        res = etree.HTML(res)
        detail_url = res.xpath('//*[@id="container"]/div[2]/div/div/div/a/@href')
        # print(detail_url)
        for i in detail_url:
            # print(i)
            detail_html = self.get_html('http://www.tuniu.com'+i)
            detail_html = etree.HTML(detail_html)
            title = detail_html.xpath('//*[@id="container"]/div[2]/div/div/div[1]/p/text()')
            if title:
                content=detail_html.xpath('//*[@id="container"]/div[2]/div/div/div[3]//text()')
                content_img=detail_html.xpath('//*[@id="container"]/div[2]/div/div/div[3]/img/@src')
                c = ''
                for j in content:
                    k = j.split()
                    for l in k:
                        c+=l
                c = c.replace('免责声明：本网转载网络文章仅为传播信息，不代表本网观点，如有侵权，请发邮件至zixun@tuniu.com联系删除。','')
                with open('./tuniu.txt','a',encoding='utf8')as f:
                    f.write(str(title)+'\n'+c+'\n'+str(content_img)+'\n'+'\n')

if __name__ == '__main__':
    for i in range(1,10):
        url = 'http://www.tuniu.com/guide/d-nanjing-1602/zixun/c0_{}/'.format(i)
        tu = TuNiuSpider()
        tu.run(url)
