import json
import re

import requests
from lxml import etree


class FacebookSpider(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'referer': 'https://www.facebook.com/Alexandersorospublic/?epa=SEARCH_BOX'
        }
        # self.url = 'https://www.facebook.com/pages_reaction_units/more/?page_id=378112989017723&cursor=%7B%22card_id%22%3A%22page_composer_card%22%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=8&referrer&fb_dtsg_ag=AQxgVhq13UqGWMnHWT-zhdntGuBHs79fs_ASn34UNE_ABA%3AAQwl23Tz_KKEEO4qeQ6T7KHsroRwifWkp9cpqCHO_EDD3w&__user=100038922504198&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozzrheCHxG3GdwIhEnUG8zFGUpxSaxu3u5EKbmbx2axuF8iBAUK7Hze3KFU9EggOdwJAAhKe-2i6pV8Gicx2q3C2W4qKm8yEqx61cxl0zV8gAwgazUtCxryo425pVE9U8oSaCzUfHGfzooAghxK5EyqEdQ9wRyXyU-9wxwnogUkBzVKey8drx67u5UiAUG2HXwACgjUC6olzaz9rx6u2bwLwBwZxG1agG4eeKi8xWbxm4UGWzU4uUyu8DxC8xK79UaoW5AbxSu68vwEy88U9o4K2G2u2WE9EjwgEmw&__req=7&__be=1&__pc=PHASED%3Aufi_home_page_pkg&dpr=1&__rev=1000921248&__s=pqowpm%3Aibho44%3Atvauxo&jazoest=27914&__spin_r=1000921248&__spin_b=trunk&__spin_t=1562723709'
        self.url = 'https://www.facebook.com/pages_reaction_units/more/?page_id=378112989017723&cursor=%7B%22card_id%22%3A%22page_posts_divider%22%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=8&fd_referrer_ui_component=feed_story&fd_referrer_ui_surface=newsfeed&fb_dtsg_ag=AQxgVhq13UqGWMnHWT-zhdntGuBHs79fs_ASn34UNE_ABA%3AAQwl23Tz_KKEEO4qeQ6T7KHsroRwifWkp9cpqCHO_EDD3w&__user=100038922504198&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozzkAjFGUqwWzob4q5-ay8WqK6otyEnCwMxqbyRyUgyEnGi4FpeuUuKcUeWDwCx138S2Sih6UXU98pDAyF8O49ElwzwKx6HBy8G6Ehwj8lg8-i49842E-7pEmUC10xmul0DwxzoGqfw-KE-dxyh166Umy9GwTgC3mbKbzUC261tx3ximfKKey8drx67u5UiAUG2HXwABojUC6olzaz9rByVU-4K2-fxm3i8xGE4ah2EgUWV8y7EK5ojyHGfwhXy9UgG5Ey6UsDxeeCzEmgK7pUox-2y8wzwBxy3a2G2u2WE9EjwgEmw&__req=n&__be=1&__pc=PHASED%3Aufi_home_page_pkg&dpr=1&__rev=1000925427&__s=%3Afev84x%3A4fz54h&jazoest=27914&__spin_r=1000925427&__spin_b=trunk&__spin_t=1562820425'
        self.cookie = {
            'sb': 'uDtjXfajXvd94A8QjMrqzU4E',
            'datr': 'uDtjXXoIBl26I0GF4bu0zi03',
            'c_user': '100038922504198',
            'xs': '32%3ABByr7qFdn4_uNQ%3A2%3A1566784562%3A-1%3A-1',
            'spin': 'r.1001100520_b.trunk_t.1566784564_s.1_v.2_',
            'fr': '0Fl8siCMrbgCISq4s.AWWeA22eBxQ9wOlXGhzjUGglZA8.BdYKAO.DE.F1j.0.0.BdYzw3.AWVm3L1R',
            'presence': 'EDvF3EtimeF1566784572EuserFA21B38922504198A2EstateFDutF1566784572526CEchFDp_5f1B38922504198F1CC',
            'wd': '1366x293',
            'act': '1566784582626%2F5',
            'pnl_data2': 'eyJhIjoib25hZnRlcmxvYWQiLCJjIjoiL2hvbWUucGhwOnRvcG5ld3MiLCJiIjpmYWxzZSwiZCI6Ii9wcm9maWxlLnBocCIsImUiOltdfQ%3D%3D',
        }

    def parse(self):
        resp = requests.get(url=self.url, headers=self.headers, cookies=self.cookie)
        print(type(resp))
        print(resp.text)
        # with open('face.json','w')as f:
        #     f.write(resp.text.replace('for (;;);',''))
        # a = re.findall(r'"><div><p>(.*?)</p><div class="',resp)
        # print(a)

        resp = resp.text.replace('for (;;);', '')
        print(resp)
        res = json.loads(resp)
        # res = res['domops'][0][3]['__html']  # content

        # 评论信息
        comment={}
        comment['comment_content'] = \
            res['jsmods']['pre_display_requires'][13][3][1]['__bbox']['result']['data']['feedback']['display_comments']['edges'][1]['node']['body']['text']
        # 评论人
        comment['comment_name']= \
            res['jsmods']['pre_display_requires'][13][3][1]['__bbox']['result']['data']['feedback']['display_comments']['edges'][1]['node']['author']['name']
        print(comment)

        res = etree.HTML(res)
        a = res.xpath('//div[@class="_5pbx userContent _3576"]//text()')[0]
        b = res.xpath('//div[@class="_4bl7"]//text()')
        b = res.xpath('//div[@_3n1k"]//text()')[0].strip()
        print(a)
        print(b)


if __name__ == '__main__':
    face = FacebookSpider()
    face.parse()
    # with open('face.json','r') as f:
    #     text = f.read()
    #     print(text)
