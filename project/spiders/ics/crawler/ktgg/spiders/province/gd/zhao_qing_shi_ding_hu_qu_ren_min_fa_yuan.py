# coding=utf-8
"""
肇庆市鼎湖区人民法院
"""


__author__ = 'wu_yong'


from ics.crawler.ktgg.spiders.base_spider.ssfwbase import SsfwBase


class ZhaoQingShiDingHuQuRenMinFaYuan(SsfwBase):
    """
    肇庆市鼎湖区人民法院, 对应ktgg项目 1531.py 爬虫
    """
    domain = 'ssfw.zqdhfy.gov.cn'
    ename = 'zhao_qing_shi_ding_hu_qu_ren_min_fa_yuan'
    cname = u'肇庆市鼎湖区人民法院'
    developer = u'吴勇'
    url_pattern = 'http://ssfw.zqdhfy.gov.cn/ktxx.aspx?cateId=15&page={}'


if __name__ == '__main__':
    seed_dict = {'ename': ZhaoQingShiDingHuQuRenMinFaYuan.ename, 'is_increment': True, 'page': 1}
    ins = ZhaoQingShiDingHuQuRenMinFaYuan(None, seed_dict)
    a = ins.start()
    print a






