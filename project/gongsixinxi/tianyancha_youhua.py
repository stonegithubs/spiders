import re

import requests
from lxml import etree

info = []


class TianYanChaSpider(object):
    def __init__(self):
        self.url = 'https://www.tianyancha.com/search?key={}'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Host': 'www.tianyancha.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.cookie = {
            'ssuid': '7867834180',
            'TYCID': '86cac5a09e3211e98b409716bc5f7457',
            'undefined': '86cac5a09e3211e98b409716bc5f7457',
            '_ga': 'GA1.2.282034658.1562227550',
            'aliyungf_tc': 'AQAAANpICUmTcwkAorbPtyqDcwiAiwrR',
            'csrfToken': 'Jjg2tlInOZnpPs5Ud9wxxrRM',
            'jsid': 'SEM-BAIDU-CG-VI-029074',
            'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1562228526,1562239657,1562288155,1562641843',
            '_gid': 'GA1.2.128552852.1562641844',
            'bannerFlag': 'true',
            'token': '6ade74d019a6472cbfae1ff2121efb54',
            '_utm': '240c174260ab40f488144f74ba97862a',
            'tyc-user-info': '%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2585%258B%25E9%2587%258C%25E6%2596%25AF%25C2%25B7%25E5%25B8%2583%25E6%259C%2597%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYzOTYzMjU5NSIsImlhdCI6MTU2MjY0MTg4MiwiZXhwIjoxNTk0MTc3ODgyfQ.wdJff-QeZJiiDXO3Pzq5kU4X-vejyCiw_3R-HzWjO0h7aXbX8M7eM6gIDvP6yPJtTJmhKWy8i_vPaYVcldVQCQ%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252216639632595%2522%257D',
            'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYzOTYzMjU5NSIsImlhdCI6MTU2MjY0MTg4MiwiZXhwIjoxNTk0MTc3ODgyfQ.wdJff-QeZJiiDXO3Pzq5kU4X-vejyCiw_3R-HzWjO0h7aXbX8M7eM6gIDvP6yPJtTJmhKWy8i_vPaYVcldVQCQ',
            'RTYCID': 'ded9aa1c4c544e769d55c904a61dcac8',
            'CT_TYCID': '178b9f0c277c4c729abe996ec91d0d4f',
            'cloud_token': '078dc2e5480744359bd083d12189a012',
            'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1562643444'
        }

    def request_html(self, company_names):

        resp = requests.get(url=self.url.format(company_names), headers=self.headers, cookies=self.cookie).text
        # with open('tianyan.html','w',encoding='utf-8')as f:
        #     f.write(resp)
        # print(resp)
        resp = etree.HTML(resp)
        # for i in range(1,10):
        # print('第'+str(i)+'家公司')
        # company_href = resp.xpath('//*[@id="web-content"]/div/div[1]/div[2]/div[2]/div['+str(i)+']/div/div[3]/div[1]/a/@href')
        # company_href = resp.xpath('//*[@id="web-content"]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[1]/a/@href')
        company_href = resp.xpath('//*[@id="web-content"]/div/div[1]/div[3]/div[2]/div[1]/div/div[3]/div[1]/a/@href')
        # print(company_href)
        company_href = company_href[0]
        return company_href

    def detail(self,company_names):
        company_href = tianyancha.request_html(company_names)
        print(company_href)
        resp_detail = requests.get(url=company_href, headers=self.headers, cookies=self.cookie).text
        renyuan = re.findall(r'target="_blank">(.*?)</a></td><td style=', resp_detail)
        zhiwei = re.findall(r'></tr></tbody></table></td><td><span>(.*?)</span></td></tr>', resp_detail)
        # with open('zjdh.html','w',encoding='utf-8')as f:
        #     f.write(resp_detail)
        detail = {}
        res = etree.HTML(resp_detail)
        detail['公司名'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[1]/h1/text()')
        detail['电话'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[1]/div[1]/span[2]/text()')
        detail['网址'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[2]/div[1]/span[2]/text()')
        detail['邮箱'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[1]/div[2]/span[2]/text')
        detail['董事'] = []
        detail['统一社会信用代码'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()')
        detail['工商注册号'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()')
        detail['组织机构代码'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[4]/text()')
        detail['公司类型'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]/text()')
        detail['简介'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[3]/span[2]/text()')
        detail['经验范围'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[11]/td[2]/span/text()')
        detail['公司地址'] = res.xpath('//*[@id="company_web_top"]/div[2]/div[3]/div[3]/div[2]/div[2]/div/div/text()')
        detail['行业'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()')
        detail['注册地址'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]/text()')
        detail['成立日期'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div/text()')
        detail['注册资本'] = res.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div/text()')

        # print(detail)
        # print('共'+str(len(renyuan))+'位主要人员')
        try:
            for i in range(len(renyuan)):
                p = zhiwei[i] + ':' + renyuan[i]
                detail['董事'].append(p)
        except Exception:
            print(detail['公司名'], '抓取主要人员出错')
        info.append(detail)


if __name__ == '__main__':
    tianyancha = TianYanChaSpider()
    tianyancha.detail('中新赛克')
    with open('res.json', 'a', encoding='utf-8')as f:
        f.write(str(info))
