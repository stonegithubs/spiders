# coding=utf-8


__author__ = 'wuyong'

from ics.crawler.ktgg.spiders.base_spider.ssfwbase import SsfwBase


class ZhaoQingShiDuanZhouQuRenMinFaYuan(SsfwBase):
    """
    肇庆市端州区人民法院, 对应ktgg项目 1530.py 爬虫
    """
    domain = 'ssfw.zqdzfy.gov.cn'
    ename = 'zhao_qing_shi_duan_zhou_qu_ren_min_fa_yuan'
    cname = u'肇庆市端州区人民法院'
    developer = u'吴勇'
    url_pattern = 'http://ssfw.zqdzfy.gov.cn/ktxx.aspx?cateId=15&page={}'


if __name__ == '__main__':
    seed_dict = {'ename': ZhaoQingShiDuanZhouQuRenMinFaYuan.ename, 'is_increment': True, 'page': 1}
    spider = ZhaoQingShiDuanZhouQuRenMinFaYuan(None, seed_dict)
    spider.start()
