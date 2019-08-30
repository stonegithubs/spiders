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
        self.url = 'https://www.gofundme.com/mvc.php?route=categorypages/load_more&page={}&term=&cid={}'
        self.headers1 = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'gdid=00-b234c7c6770c40a898d31f2a0b64ca53-71ac06a8; _gcl_au=1.1.1617081926.1566613509; _ga=GA1.2.1457700540.1566613509; _cb_ls=1; _cb=BURQ7ZBKBAQC4I7Po; _fbp=fb.1.1566613515850.429672311; fv={"t":1566618277,"fid":34666278}; suid=57a52c56514d493eba24fb8faba34fe4; _gid=GA1.2.622431087.1566782275; referer=https%3A%2F%2Fwww.gofundme.com%2Fdiscover%2Fmedical-fundraiser; fuid=a7d87aa8bb4447c1a7075d8ab9a30f4a; visitor=%7B%22country%22%3A%22CN%22%2C%22locale%22%3A%22en_US%22%2C%22cookieWarning%22%3A%220%22%7D; flow=%7B%22DONATION%22%3A%22d_ex%22%7D; fingerprints=%7B%22fingerprints%22%3A%5B%222de5dd0162664bc1dceda5f6a0a6ab82%22%5D%2C%22userAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36%22%7D; rvc=a%3A5%3A%7Bi%3A34666278%3Bi%3A1566783530%3Bi%3A33481342%3Bi%3A1566783303%3Bi%3A34291596%3Bi%3A1566801308%3Bi%3A33410424%3Bi%3A1566804575%3Bi%3A34200352%3Bi%3A1566802725%3B%7D; mp_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoiZ29mdW5kbWUtZmFzdHRyYWNrIiwiaW5wdXRMYWJlbCI6Ik1vYmlsZV9TREsiLCJpbnB1dFR5cGUiOiJKU1NESyJ9.VcK4Qu7IFdx-4eaNvFpO6-k7uLU4BnnoCaUKfLDYXBM_mixpanel=%7B%22distinct_id%22%3A%20%2200-b234c7c6770c40a898d31f2a0b64ca53-71ac06a8%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; mp_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoiZ29mdW5kbWUtZmFzdHRyYWNrIiwiaW5wdXRMYWJlbCI6ImpzX2ltcHJlc3Npb25zIiwiaW5wdXRUeXBlIjoiSlNTREsifQ.b5cv2xeiayTkWNVbv-Hg9BGILIHwgE1nL2Tl2OaPVIA_mixpanel=%7B%22distinct_id%22%3A%20%2200-b234c7c6770c40a898d31f2a0b64ca53-71ac06a8%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36%22%7D; _chartbeat2=.1566613515721.1566804594794.101.CoKisHDsPlF4CQIDLFD9d-eQCd9WrG.1; _cb_svref=null; mp_default__c=111; mp_default__c3=118814; mp_default__c4=112723; mp_default__c5=546; mp_impression__c=111; mp_impression__c3=118814; mp_impression__c4=112723; mp_impression__c5=546; ssid1=247add1134-b233c60642bb4c90-5%3A1566807038; ssid2=2479be8100-0178d8d410514434-5%3A1566978038',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }

    def run(self, i, index):
        print(4)
        try:
            res = requests.get(self.url.format(i, index), self.headers, timeout=3).text
        except:
            res = ''
            print('连接失败，正在重连')
            time.sleep(1)
            self.run(i, index)
        print(5)
        if res:
            res = etree.HTML(res)
            url_list = res.xpath('//div/div/a[1]/@href')  # 获取列表页url
            print(url_list)
            url_list = url_list[::2]  # 由于获取到的url 1，2是重复的，so，取步长2
            for j in url_list:  # 进入详情页
                try:
                    detail_html1 = requests.get(j, self.headers)
                    url = j.replace('https://www.gofundme.com/', '')
                    detail_html1 = detail_html1.text
                except Exception as err:
                    print(6)

                    detail_html1 = ''
                    self.run(i, index)
                # with open('./list_page.html','w',encoding='utf8')as de:
                #     de.write(detail_html)
                detail_html = etree.HTML(detail_html1)
                title = detail_html.xpath('//h1/text()')[0]  # 项目名称
                print(1, title)
                money1 = detail_html.xpath('//h2//text()')  # 项目资金
                try:
                    money = money1[0]
                except:
                    money = ''
                if '\n' in money:
                    money = money1[1]
                with open('data.txt', 'a+', encoding='utf8')as f:
                    f.write('\n' + str(title) + '^' + str(money))
                # print(money)
                # break
                juan_kuan_ren = re.findall(r':0,"url":"(.*?)","', detail_html1)  # 捐款详情url拼接字符串
                if juan_kuan_ren:
                    print(3)
                    juan_kuan_url = 'https://gateway.gofundme.com/web-gateway/v1/feed/' + juan_kuan_ren[
                        0] + '/donations?limit=1000&offset={}'  # 拼接后捐款人url
                    # self.get_juan_kuan(juan_kuan_url, i, index)
                    for h in range(1000, 1000000, 1000):
                        try:
                            juan_kuan_info = requests.get(juan_kuan_url.format(h), self.headers).text
                        except:
                            juan_kuan_info = ''
                            self.run(i, index)
                        try:
                            juan_info = json.loads(juan_kuan_info)
                        except Exception:
                            juan_info = ''
                            self.run(i, index)
                        # print(juan_info['references']['donations'])
                        # print(len(juan_info['references']['donations']))
                        detail_info = juan_info['references']['donations']
                        for l in detail_info:
                            jin_e = l['amount']
                            ni_cheng = l['name']
                            # print(ni_cheng)
                            # print(jin_e)
                            with open('data.txt', 'a+', encoding='utf8')as f:
                                f.write('^' + str(ni_cheng) + '^' + str(jin_e))
                        if juan_info['meta']['has_next'] == 'true':
                            continue
                        # else:
                        #     break
                else:
                    print(2)
                    for g in range(0, 500, 10):
                        juan_kuan_url = 'https://www.gofundme.com/mvc.php?route=donate/pagingDonationsFoundation&url={}&idx={}&type=recent'.format(
                            url, g)
                        # juan_kuan_url = 'https://www.gofundme.com/mvc.php?route=donate/pagingDonationsFoundation&url=help-taki-win-his-battle-withcancer&idx=0&type=recent'
                        print(7, juan_kuan_url)
                        resp = requests.get(juan_kuan_url, self.headers1).text
                        element = etree.HTML(resp)
                        try:
                            ni_cheng1 = element.xpath('//div[@class="supporter-name"]/text()')
                            print(8,ni_cheng)
                        except Exception:
                            break
                        jin_e1 = element.xpath('//div[@class="supporter-amount"]/text()')
                        for x in range(len(jin_e1)):
                            try:
                                ni_cheng = ni_cheng1[x]
                                jin_e = jin_e1[x]
                            except:
                                break
                            with open('data.txt', 'a+', encoding='utf8')as f:
                                f.write('^' + str(ni_cheng) + '^' + str(jin_e))
            return res
        else:
            return 0

    # def get_juan_kuan(self, juan_kuan_url, i, index):
    #     # juan_kuan_url = 'https://gateway.gofundme.com/web-gateway/v1/feed/rette-valeria/donations?limit=100&offset=0'
    #     # print(i)
    #     for i in range(1000, 1000000, 1000):
    #         try:
    #             juan_kuan_info = requests.get(juan_kuan_url.format(i), self.headers).text
    #         except:
    #             juan_kuan_info = ''
    #             self.run(i, index)
    #         try:
    #             juan_info = json.loads(juan_kuan_info)
    #         except Exception:
    #             juan_info = ''
    #             self.run(i, index)
    #         # print(juan_info['references']['donations'])
    #         # print(len(juan_info['references']['donations']))
    #         detail_info = juan_info['references']['donations']
    #         for l in detail_info:
    #             ni_cheng = l['amount']
    #             jin_e = l['name']
    #             print(ni_cheng)
    #             print(jin_e)
    #         if juan_info['meta']['has_next'] == 'true':
    #             continue
    #         else:
    #             break

    def start(self, index):
        for i in range(1, 100):
            print(i)
            res = zhongchou.run(i, index)
            if res == '':
                break

    def wrap(self):
        """大列表"""
        index = ['11', '9', '2', '13', '17', '3', '5', '7', '19', '8', '6', '12', '4', '14', '16', '10', '18', '25']
        for index in index:
            self.start(index)


if __name__ == '__main__':
    zhongchou = ZhongChouSpider()
    zhongchou.wrap()
    # name = ['a', 'b', 'c', 'd', 'e']
    # for j, i in enumerate(name):
    #     print(i)
    #     print(j + 1)