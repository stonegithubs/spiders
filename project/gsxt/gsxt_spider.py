import json
import random
import time
from collections.abc import Iterable
from multiprocessing import Pool

import requests

from gsxt.sql_utils import MysqlUtil, MongoUtil

UA = [
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
]


class Gsxt(object):
    config = {
        'host': '218.94.82.249',
        'port': 8015,  # MySQL默认端口
        'user': 'rhino',  # mysql默认用户名
        'password': 'rhino',
        'db': 'company_list',  # 数据库
        'use_unicode': True,
        'charset': 'utf8',
    }
    url = 'https://app.gsxt.gov.cn/gsxt/corp-query-app-search-1.html'
    sql_conn = MysqlUtil(**config)
    nosql_conn = MongoUtil('GSXT', 'localhost', 27017)
    method = 'direct'
    sleeptime = random.uniform(1, 2)
    tunnel = random.randint(1, 10000)
    temp1 = 0
    temp2 = 0
    info = {}
    item = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Proxy-Tunnel": str(tunnel)
    }

    # def getIp(self):
    #     req_ip = requests.get(
    #         'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&pack=37176&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=').text

    #     proxies = {"https": req_ip.strip()}
    #     print('*****当前IP*****{}'.format(proxies))
    #     return proxies

    def getIp(self):
        # 代理服务器
        proxyHost = "u2999.10.tn.16yun.cn"
        proxyPort = "6442"
        # 代理隧道验证信息
        proxyUser = "16VNOVSV"
        proxyPass = "050601"
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        # 设置 http和https访问都是用HTTP代理
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def start_company_query(self, keyword):
        self.temp1 = self.temp1 + 1
        if self.temp1 >= 10:
            sql = "update Data_Minglu_Company set checkstatus = 2 where checkstatus = 6 and entName='{}'and sf = 'jiangsu'".format(
                keyword)
            self.sql_conn.update(sql)
            print("query company times limit.")
            return None

        try:
            q_data = 'conditions={"excep_tab":"0","ill_tab":"0","area":"0","cStatus":"0","xzxk":"0","xzcf":"0","dydj":"0"}&searchword=' + keyword + '&sourceType=W'
            if self.method == 'direct':
                resp = requests.post(self.url, data=q_data.encode('utf8'), headers=self.headers, timeout=20)
            else:
                proxies = self.getIp()
                resp = requests.post(self.url, data=q_data.encode('utf8'), proxies=proxies, headers=self.headers,
                                     timeout=20)
                resp.encoding = resp.apparent_encoding

            text = resp.text
            print(keyword, text)
            if text.find("由于您操作过于频繁") != -1:
                print('-----由于您操作过于频繁---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("设置为拦截") != -1:
                print('-----当前访问疑似黑客攻击，已被网站管理员设置为拦截------重试start_company_query------')
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("data") == -1 and text.find("result") == -1 and text.find("anCheYear") != -1 and text == "[]":
                print('-----没有返回数据1---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("\"data\":[]") != -1 or text.find("\'data\':{}") != -1 or text.find("\"data\":{}") != -1:
                print('-----没有返回数据2---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("<!DOCTYPE html>") != -1 or text.find("<html>") != -1:
                print('-----网页异常---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("503 Service Temporarily Unavailable") != -1:
                print('-----503 Service Temporarily Unavailable---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("502 Bad Gateway") != -1:
                print('-----502 Bad Gateway---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)

            if text.find("Too Many Requests") != -1:
                print('-----代理问题---{}---重试start_company_query------'.format(keyword))
                time.sleep(self.sleeptime)
                text = self.start_company_query(keyword)
        except:
            print('-----连接异常---{}---重试start_company_query------'.format(keyword))
            text = self.start_company_query(keyword)
        return text

    def query_info(self, prefix, pripid, company):
        url = "https://app.gsxt.gov.cn/gsxt/" + prefix + pripid + ""
        if prefix != 'corp-query-entprise-info-primaryinfoapp-annualReportInfo-':
            self.temp2 = self.temp2 + 1
        if self.temp2 >= 10:
            print("query company detail info times limit.")
            return None
        try:
            proxies = self.getIp()
            resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=5)
            resp.encoding = resp.apparent_encoding
            text = resp.text
            # print(company, text)

            if text.find("由于您操作过于频繁") != -1:
                print(company, prefix, "由于您操作过于频繁", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("设置为拦截") != -1:
                print(company, prefix, "当前访问疑似黑客攻击，已被网站管理员设置为拦截-", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("<!DOCTYPE html>") != -1 or text.find("<html>") != -1:
                print(company, prefix, "网页异常", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("503 Service Temporarily Unavailable") != -1:
                print(company, prefix, "503 Service Temporarily Unavailable", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("502 Bad Gateway") != -1:
                print(company, prefix, "502 Bad Gateway", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("Error report") != -1:
                print(company, prefix, "Error report", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("result") == -1 and text.find("data") == -1 and text == "[]":
                print(company, prefix, "没有返回数据1", "重试")
                time.sleep(1)
                if text.find("For input string:") != -1:
                    pass
                elif text.find("Status 500") != -1:
                    pass
                else:
                    text = self.query_info(prefix, pripid, company)

            if text.find("\"data\":[]") != -1 or text.find("\'data\':{}") != -1 or text.find("\"data\":{}") != -1:
                print(company, prefix, "没有返回数据2", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)

            if text.find("Too Many Requests") != -1:
                print(company, prefix, "代理问题", "重试")
                time.sleep(1)
                text = self.query_info(prefix, pripid, company)
        except:
            print(company, prefix, "连接异常", "重试")
            time.sleep(1)
            text = self.query_info(prefix, pripid, company)
        return text

    def get_sub_id(self, text):
        pripid = []
        if not text and text.find('result') != -1:
            text = text.replace("<font color=red>", "").replace("</font>", "")
            text = text.replace("&nbsp;", "").replace('null', 'None')
            js = json.loads(json.dumps(eval(text)))
            data_arr = js.get('data').get('result').get('data')
            for each in data_arr:
                name = each.get("entName").replace("&nbsp;", "")
                pripid.append(each.get("pripid") + ".html?nodeNum=" + str(each.get("nodeNum")) + "&entType=" + str(
                    each.get("entType")) + "&sourceType=W")
        # print(pripid)
        return pripid

    def get_sub_info(self, pripid, type, company):
        prefix = None
        self.temp2 = 0
        if type == 'base': prefix = 'corp-query-entprise-info-primaryinfoapp-entbaseInfo-'
        if type == "KeyPerson": prefix = 'corp-query-entprise-info-KeyPerson-'
        if type == "alter": prefix = 'corp-query-entprise-info-alter-'
        if type == "shareholder": prefix = 'corp-query-entprise-info-shareholder-'
        if type == 'branch': prefix = 'corp-query-entprise-info-branch-'
        if type == 'stakqualitinfo': prefix = 'corp-query-entprise-info-stakqualitinfo-'
        if type == 'trademark': prefix = 'corp-query-entprise-info-trademark-'
        if type == 'licenceinfoDetail': prefix = 'corp-query-entprise-info-licenceinfoDetail-'
        if type == 'anCheYearInfo': prefix = 'corp-query-entprise-info-anCheYearInfo-'

        ent_info = self.query_info(prefix, pripid, company)
        # print(ent_info)
        return ent_info

    def get_sub_pripid(self, text):
        if not text and text.find('result') != -1:
            text = text.replace("<font color=red>", "").replace("</font>", "")
            text = text.replace("&nbsp;", "").replace('null', 'None')
            js = json.loads(json.dumps(eval(text)))
            data_arr = js.get('data').get('result').get('data')
            for each in data_arr:
                name = each.get("entName").replace("&nbsp;", "")
                pripid = each.get("pripid") + ".html?nodeNum=" + str(each.get("nodeNum")) + "&entType=" + str(
                    each.get("entType")) + "&sourceType=W"
                yield pripid, name

    def get_year_report_pripid(self, id, item):
        pripid = id + "&anCheId=" + item.get("anCheId") + "&anCheYear=" + item.get("anCheYear").replace("&quot;", "")
        # pripid.append(id)
        print('**year_report_pripid**{}'.format(pripid))
        return pripid

    def get_year_report(self, pripid, company):
        prefix = 'corp-query-entprise-info-primaryinfoapp-annualReportInfo-'
        ent_info = self.query_info(prefix, pripid, company)
        return ent_info

    def sub_info(self, text, company):
        if not text:
            print("sub info None {}".format(company))
            return None
        # 公司其他信息
        try:
            for sub_pripid in self.get_sub_pripid(text):
                # print(sub_pripid)
                base_info = self.get_sub_info(sub_pripid[0], 'base', company)
                print('base_info:{}'.format(base_info))
                KeyPerson_info = self.get_sub_info(sub_pripid[0], 'KeyPerson', company)
                print('KeyPerson_info:{}'.format(KeyPerson_info))
                alter_info = self.get_sub_info(sub_pripid[0], 'alter')
                print('alter_info:{}'.format(alter_info))
                shareholder_info = self.get_sub_info(sub_pripid[0], 'shareholder', company)
                print('shareholder_info:{}'.format(shareholder_info))
                branch_info = self.get_sub_info(sub_pripid[0], 'branch')
                print('branch_info:{}'.format(branch_info))
                stakqualitinfo_info = self.get_sub_info(sub_pripid[0], 'stakqualitinfo', company)
                print('stakqualitinfo_info:{}'.format(stakqualitinfo_info))
                trademark_info = self.get_sub_info(sub_pripid[0], 'trademark')
                print('trademark_info:{}'.format(trademark_info))
                licenceinfoDetail_info = self.get_sub_info(sub_pripid[0], 'licenceinfoDetail', company)
                print('licenceinfoDetail_info:{}'.format(licenceinfoDetail_info))
                anCheYearInfo_info = self.get_sub_info(sub_pripid[0], 'anCheYearInfo', company)
                print('anCheYearInfo_info:{}'.format(anCheYearInfo_info))
                self.info[sub_pripid[1]]['base_info'] = base_info
                self.info[sub_pripid[1]]['alter_info'] = alter_info
                self.info[sub_pripid[1]]['KeyPerson_info'] = KeyPerson_info
                self.info[sub_pripid[1]]['shareholder_info'] = shareholder_info
                self.info[sub_pripid[1]]['branch_info'] = branch_info
                self.info[sub_pripid[1]]['stakqualitinfo_info'] = stakqualitinfo_info
                self.info[sub_pripid[1]]['trademark_info'] = trademark_info
                self.info[sub_pripid[1]]['licenceinfoDetail_info'] = licenceinfoDetail_info
                self.info[sub_pripid[1]]['anCheYearInfo_info'] = anCheYearInfo_info

                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]}, {'$set': {'base_info': base_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]}, {'$set': {'alter_info': alter_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]}, {'$set': {'KeyPerson_info': KeyPerson_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]}, {'$set': {'branch_info': branch_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]},
                                       {'$set': {'stakqualitinfo_info': stakqualitinfo_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]}, {'$set': {'trademark_info': trademark_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]},
                                       {'$set': {'licenceinfoDetail_info': licenceinfoDetail_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]},
                                       {'$set': {'licenceinfoDetail_info': licenceinfoDetail_info}})
                self.nosql_conn.update('gsxt', {'name': sub_pripid[1]},
                                       {'$set': {'anCheYearInfo_info': anCheYearInfo_info}})
        except Exception as e:
            print(e)

    def yeareport_info(self, text, company):
        # 年报：同一个公司有多个年报
        if not text and text.find('result') != -1:
            text = text.replace("<font color=red>", "").replace("</font>", "")
            text = text.replace("&nbsp;", "").replace('null', 'None')
            js = json.loads(json.dumps(eval(text)))
            data_arr = js.get('data').get('result').get('data')
            for each in data_arr:
                # year_report_info = []
                name = each.get("entName").replace("&nbsp;", "")
                self.info[name] = {}
                self.info[name]['年报'] = {}
                self.item['year_report'] = {}
                id = each.get("pripid") + ".html?nodeNum=" + str(each.get("nodeNum")) + "&entType=" + str(
                    each.get("entType")) + "&sourceType=W"
                ent_info = self.query_info('corp-query-entprise-info-anCheYearInfo-', id, company)
                try:
                    datas = json.loads(ent_info)
                    # print('+++++++++datas=++++++++{}'.format(datas))
                except:
                    print('+++ent_info is None+++')
                    self.info[name]['年报'] = 'null'
                    continue
                if isinstance(datas, Iterable):
                    for it in datas:
                        year_report_pripid = self.get_year_report_pripid(id, it)
                        year_report_info = self.get_year_report(year_report_pripid, company)
                        print('**year_report_info**{}'.format(year_report_info))
                        year = year_report_pripid[-4:]
                        print('**year**{}'.format(year))
                        self.info[name]['年报'][year] = year_report_info
                        self.item['name'] = name
                        self.item['year_report'][year] = year_report_info
                    self.nosql_conn.update('gsxt', {'name': name}, {'$set': self.item})

    def run(self, record):
        company = record[1]
        print("------开始-------{}------".format(company))
        text = self.start_company_query(company)
        if not text:
            self.yeareport_info(text, company)
            self.sub_info(text, company)
            print('**{}*info***{}'.format(company, self.info))
            # with open('ZXSK_demon.txt', 'w+', encoding='utf-8') as f:
            #     f.write(str(self.info))


if __name__ == '__main__':
    while True:
        p = Pool(10)  # 开辟进程池
        gsxt = Gsxt()
        update_sql = "update Data_Minglu_Company set checkstatus = 6 where checkstatus = 0 and entName is not null and sf = 'jiangsu' limit 6"
        gsxt.sql_conn.update(update_sql)
        query_sql = "select * from Data_Minglu_Company where checkstatus = 6 limit 20;"
        cnt, rets = gsxt.sql_conn.query(query_sql)
        if rets:
            for i in rets:
                p.apply_async(gsxt.run, args=(i,))  # 每个进程都调用Tomongo函数，
            print('Waiting for all subprocesses done ...')

        p.close()  # 关闭进程池
        p.join()
    # query_sql = "select * from Data_Minglu_Company where entName='南京中新赛克科技有限责任公司';"
    # cnt, rets = gsxt.sql_conn.query(query_sql)
    # if rets:

    #     for i in rets:
    #         gsxt.run(i)
    #     print('Waiting for all subprocesses done ...')
