import json
import re
import time
import requests
from lxml import etree
from requests.packages import urllib3

urllib3.disable_warnings()


class ZhongChouSpider(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

    def run(self):
        j = 'https://www.gofundme.com/f/uk-ad-campaign-to-defend-sinobritish-jd'
        try:
            detail_html1 = requests.get(j, self.headers).text
        except Exception:
            print(6)
            detail_html1 = ''
            self.run()
        detail_html = etree.HTML(detail_html1)
        title = detail_html.xpath('//h1/text()')[0]  # 项目名称
        print(1, title)
        money1 = detail_html.xpath('//h2//text()')  # 项目资金
        # with open('data1.txt', 'a+', encoding='utf8')as f:
        #     f.write('\n' + str(title) + '^' + str(money1[0]))
        juan_kuan_url = 'https://gateway.gofundme.com/web-gateway/v1/feed/uk-ad-campaign-to-defend-sinobritish-jd/donations?limit=1000&offset={}'  # 拼接后捐款人url
        for h in range(0, 1000000, 1000):
            print(h)
            try:
                juan_kuan_info = requests.get(juan_kuan_url.format(h), self.headers).text
            except:
                print('请求失败，重新请求')
                time.sleep(5)
                juan_kuan_info = requests.get(juan_kuan_url.format(h), self.headers).text
            juan_info = json.loads(juan_kuan_info)
            detail_info = juan_info['references']['donations']
            for l in detail_info:
                jin_e = l['amount']
                ni_cheng = l['name']
                if ni_cheng == 'Anonymous' or ni_cheng == 'Anonymous Anonymous' or ni_cheng == '  Anonymous' or ni_cheng == ' Anonymous   Anonymous ' or ni_cheng == 'Anonymous  Anonymous ' or ni_cheng == ' Anonymous Anonymous':
                    continue
                with open('data.txt', 'a+', encoding='utf8')as f:
                    f.write('zhong ying lian he sheng ming deng bao' + '^' + str(money1[0]) + '^' + str(
                        ni_cheng) + '^' + str(jin_e) + '\n')
            if juan_info['meta']['has_next'] == 'true':
                continue
            # else:
            #     break


if __name__ == '__main__':
    zhongchou = ZhongChouSpider()
    zhongchou.run()
