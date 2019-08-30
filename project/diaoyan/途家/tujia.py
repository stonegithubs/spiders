import json

import requests


class TuJiaSpider(object):
    def __init__(self):
        self.url = 'https://www.tujia.com/bingo/pc/search/searchUnit'
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '247',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'Qs_lvt_317639=1564125077; tujia_out_site_landingUrl=https%3A%2F%2Fwww.tujia.com%2F%3Futm_source%3Dbaidu%26utm_medium%3Dcpc%26utm_term%3Dbdpztitle; tujia_out_site_referrerUrl=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00f7nZK_0yS-b0KMAR0aHG1GI00000cgNP-C00000VtSvCC.THLPEo1i0A3qmh7GuZR0T1Y3myRLujbYnW0snhcYrAmY0ZRqfHfdfYfvf19jPRcsnH-DnHcvnDwaPW-AfW-7wW9AnYn0mHdL5iuVmv-b5HnzP1csrjT1Pj6hTZFEuA-b5HDv0ARqpZwYTZnlQzqLILT8IZNJpyD8mvqVQ1qdIAdxTvqdThP-5yF9pywdFMNYUNqVuywGIyYqmLKWFMNYUNqYugFV5yFbTZGYpgw_ufKWThnqP10YPf%26tpl%3Dtpl_11534_19968_16032%26l%3D1513543045%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E9%252580%252594%2525E5%2525AE%2525B6%2525E6%2525B0%252591%2525E5%2525AE%2525BF%2525E5%2525AE%252598%2525E7%2525BD%252591--%2525E9%2525AB%252598%2525E5%252593%252581%2525E8%2525B4%2525A8%2525E6%2525B0%252591%2525E5%2525AE%2525BF%25257C%2525E5%2525AE%2525A2%2525E6%2525A0%252588%25257C%2525E5%252588%2525AB%2525E5%2525A2%252585%25257C%2525E7%25259F%2525AD%2525E7%2525A7%25259F%2525E9%2525A2%252584%2525E8%2525AE%2525A2%2525E5%2525B9%2525B3%2525E5%25258F%2525B0.%2526xp%253Did(%252522m3272087348_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D117%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E9%2580%2594%25E5%25AE%25B6%26oq%3D%2525E8%252589%2525BA%2525E9%2525BE%252599%26rqlang%3Dcn%26inputT%3D2477; tujia_utm=baidu; mediav=%7B%22eid%22%3A%22201876%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22v%60(2nESvC%23%3A%5ESnF%247oyo%22%2C%22ctn%22%3A%22%22%7D; tujia.com_PortalContext_UserId=0; tujia.com_PortalContext_RefUrl=https://www.tujia.com/?utm_source=baidu&utm_medium=cpc&utm_term=bdpztitle; tujia.com_PortalContext_LongerRefUrl=https://www.tujia.com/?utm_source=baidu&utm_medium=cpc&utm_term=bdpztitle; tujia.com_PortalContext_GuestToken=97102282-b189-40e9-9dad-387dcc68f9fc; tujia.com_PortalContext_GuestId=-513368727; tujia.com_PortalContext_LandingUrl=http://www.tujia.com/api/pchome/homepage?utm_source=baidu&utm_medium=cpc&utm_term=bdpztitle; tujia.com_PortalContext_GuestCount=0; tujia.com_PortalContext_BedCount=0; tujia.com_PortalContext_RoomCount=0; tujia.com_PortalContext_UserToken=00000000-0000-0000-0000-000000000000; tujia.com_PortalContext_StartDate=2019-7-26; tujia.com_PortalContext_EndDate=2019-7-27; gr_user_id=4558b4ea-ee6a-4278-937a-d9e96eb106ae; gr_session_id_1fa38dc3b3e047ffa08b14193945e261=3ba412c2-794f-4fa5-80db-16925ba717a6; gr_cs1_3ba412c2-794f-4fa5-80db-16925ba717a6=user_id%3A0; qimo_seosource_797098a0-b29d-11e5-b3b1-49764155fe50=%E5%85%B6%E4%BB%96%E7%BD%91%E7%AB%99; qimo_seokeywords_797098a0-b29d-11e5-b3b1-49764155fe50=%E6%9C%AA%E7%9F%A5; href=https%3A%2F%2Fwww.tujia.com%2F%3Futm_source%3Dbaidu%26utm_medium%3Dcpc%26utm_term%3Dbdpztitle; accessId=797098a0-b29d-11e5-b3b1-49764155fe50; gr_session_id_1fa38dc3b3e047ffa08b14193945e261_3ba412c2-794f-4fa5-80db-16925ba717a6=true; bad_id797098a0-b29d-11e5-b3b1-49764155fe50=91c2f151-af74-11e9-90d4-6b51b220add0; nice_id797098a0-b29d-11e5-b3b1-49764155fe50=91c2f152-af74-11e9-90d4-6b51b220add0; tujia.com_PortalContext_DestinationId=9; Qs_pv_317639=3971534307331444000%2C818409198294981200; pageViewNum=2; manualclose=1; tujia.com_PortalContext_CssToken=TfONKbMRe/+trzHIjoEPeiQi0ojphRCz6t79kWvRai4=',
            'Host': 'www.tujia.com',
            'Origin': 'https://www.tujia.com',
            'Referer': 'https://www.tujia.com/unitlist?startDate=2019-07-26&endDate=2019-07-27&cityId=9&ssr=off',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

        self.data = {
            'callCenter': 'false',
            'conditions': '[{gType: 0, type: 42, value: "9"}, {gType: 0, label: null, type: 47, value: "2019-07-26,2019-07-27"}]',
            'pageIndex': 1,
            'pageSize': 9,
            'returnAllConditions': 'true',
            'returnRedPacketInfo': 'true',
            'returnUnitTagBadgeInfo': 'true',
        }
        self.data = json.dumps(self.data)

    def get_html(self):
        resp = requests.post(url=self.url, headers=self.headers, data=self.data)
        resp = resp.json()
        resp = json.dumps(resp)
        json.loads(resp)
        return resp

    def run(self):
        all_json = self.get_html()
        print(all_json)


if __name__ == '__main__':
    # a = {'conditions': '[{gType: 0, type: 42, value: "9"}, {gType: 0, label: null, type: 47, value: "2019-07-26,2019-07-27"}]',
    # }
    #     a = json.dumps(a)
    #     print(a)
    tu = TuJiaSpider()
    tu.run()
