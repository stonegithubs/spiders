import requests
from lxml import etree

class BoosSpider(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers).text
        return res

    def etree_html(self, html):
        htmls = etree.HTML(html)
        return htmls

    def string_Handle(self, str):
        l = ''
        c = ''
        for i in str:
            l += i
        # print(l.split()[0])
        for j in l.split():
            c += j
        return c

    def run(self, url):
        job = []
        while True:
            if url:
                all_html = self.get_html('https://www.zhipin.com' + url)
                print(1)
                print('https://www.zhipin.com' + url)
                all_html = self.etree_html(all_html)
                # detail_url = all_html.xpath('//div[@class="job-list"]/ul/li/div/div/h3/a/@href')
                detail_url=all_html.xpath('//*[@id="main"]/div/div[3]/ul/li[1]/div/div[1]/h3/a/div[1]')
                print(detail_url)
                for i in detail_url:
                    job_info = {}
                    detail_html = self.get_html('https://www.zhipin.com' + i)
                    detail_html = self.etree_html(detail_html)
                    job_info['job_title'] = detail_html.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()')[
                        0]
                    job_info['job_price'] = \
                        detail_html.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()')[0]
                    try:
                        job_info['compny_info'] = \
                            detail_html.xpath('//div[@class="job-sec"]/div[@class="name"]/text()')[0]
                    except Exception:
                        job_info['compny_info'] = ''
                    job_info['job_compny'] = \
                        detail_html.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/div/a[2]/text()')[0].split()[0]
                    job_compny = detail_html.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()')
                    job_info['work_duty'] = self.string_Handle(job_compny)
                    job.append(job_info)
                url = self.get_next_pag('https://www.zhipin.com' + url)
            else:
                break
        print(job)
        with open('./boos.json','w',encoding='utf8')as f:
            f.write(str(job))

    def get_next_pag(self, url):
        res = self.get_html(url)
        res = self.etree_html(res)
        try:
            next_url = res.xpath('//div[@class="page"]/a[@class="next"]/@href')[0]
        except Exception:
            next_url = ''
            print('没有下一页')
        # next_url = next_url
        return next_url


if __name__ == '__main__':
    url = '/c101190100/?query=python&page=1'
    tu = BoosSpider()
    tu.run(url)
