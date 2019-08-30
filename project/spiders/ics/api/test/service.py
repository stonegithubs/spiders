#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4

__author__ = 'MaoJingwen'

from ics.scheduler import app
import time

# seed_dict = {
#     'ics_name': '张三',
#     'ics_no': '',
#     'ics_type': '',
# }

seed_dict = {"task_name":"zhixing","task_id":str(uuid4()),"target_name":"张三保","target_id": "","target_type":0}
app.send_task('ics.task.zhixing.cdrcb.task.start',[seed_dict],queue='queue_cdrcb_normal_zhixing_test_wa', priority=0)


# seed_dict = {
#     'company_name': '湖南临武舜华',
#     'company_zch': '',
# }
# app.send_task('ics.task.zhixing.task.get_page_cnt',[seed_dict],queue='wuyong_test_zhixing', priority=0)

# 湖南临武舜华
# for i in range(100):
#     app.send_task('ics.task.test.task.multi',[2,2],queue='wuyong_test_queue', priority=0)
# for i in range(1000):
#     app.send_task('ics.task.test.task.multi',[2,3],queue='maojingwen_queue', priority=9)


# app.send_task('ics.task.test.task.print_str',["陈坚"],queue='maojingwen_queue', priority=9)

# app.send_task('ics.task.test.task.test_stable', ["小小", "命名", "cc"], queue='mjw_test_queue')

# from ics.task.test.task import multi
#
# # multi.apply_async(args=(2, 2),queue='priority', priority=0)
#
# for i in range(100):
#     multi.apply_async(args=(2, 2),queue='tasks', priority=0)
# for i in range(100):
#     multi.apply_async(args=(2, 3),queue='tasks', priority=9)

# from ics.task.example.tuliu_task import start
# start.delay()

# from ics.task.example.baidu_news_task import start
# start.delay('冰鉴')

# from ics.task.core import send_download_request
# from ics.http import Request
#
# request = Request(url='https://img1s.tuliu.com/art/2018/05/22/5b03cc29d9c1b_mid.jpg',
#                   meta={'img_name': 'test.jpg'}, is_img=True, callback='ics.task.example.tuliu_task.process_pic')
# send_download_request(request,'tuliu_queue')

# from ics.scheduler import app
#
# for i in range(0, 1000):
#     app.send_task('ics.task.test.task.add', [i, 3], queue='test_queue')

# from ics.task.example.tuliu_task import start
# result = start.delay()


# chain_x = multi.s(2,2) | multi.s(4) | add.s(7)
# for i in range(1000):
#     chain_x()

# res = chain(add.s(2,2), add.s(4), multi.s(8))()
#
# print res.get()


# chain_x = add.s(2,2) | add.s(4) | multi.s(7)
# print chain_x().get()

# list_c = ['四川擎旭建筑工程有限公司',
# '四川赛煌商贸有限公司',
# '广汉天益冶金有限责任公司',
# '四川腾聪科技发展有限公司',
# '四川省金坤源劳务有限公司',
# '四川众和源餐饮管理有限公司',
# '四川东拓贸易有限公司',
# '四川美辰节能工程有限公司',
# '成都源合元汽车销售有限公司',
# '四川时尚丰汽车销售服务有限公司',
# '成都奥纳斯特科技有限责任公司',
# '绿地集团四川申宏置业有限公司',
# '四川瑞基建设工程有限公司',
# '成都龙魂华韵文化传播有限公司',
# '成都天益远洋国际贸易有限公司',
# '成都合众动保商贸有限公司',
# '成都市温江钟鸣实业有限责任公司',
# '成都英杰机械有限责任公司',
# '成都京蓉物流有限公司',
# '四川海思出租汽车有限公司',
# '四川汇荣合商贸有限公司',
# '成都益海矿业有限公司',
# '成都熹善文化创意策划有限公司',
# '四川中轮环保索具有限公司',
# '成都易屋之家科技有限公司',
# '四川圣吉菲汽车贸易有限公司',
# '中电国采诚泰实业有限公司',
# '四川新华蜀物流有限公司',
# '四川世华博爱旅游资源开发有限公司',
# '达州圆梦园集群生态农业有限公司',
# '成都天行建科技有限公司',
# '成都兰木韵园艺有限公司',
# '四川全富商贸有限公司',
# '重庆国恩科技发展有限公司成都分公司',
# '四川果州投资管理有限公司',
# '成都市美生达贸易有限公司',
# '攀枝花市东区锦川商贸经营部',
# '成都伟能科技有限公司',
# '四川省华友盛世装饰有限公司',
# '宣汉县云峰砼业有限公司',
# '成都市众托包装有限公司',
# '崇州市合力建材有限公司',
# '四川万汇天达房地产开发有限公司',
# '崇州佳颖天合电子商务有限公司',
# '成都茗森家具有限公司',
# '四川劲椹食品科技有限公司',
# '成都市羊马新城玫瑰园开发有限公司',
# '成都三枫农业开发有限公司',
# '成都金彭世家餐饮管理有限公司',
# '成都市鑫世发建材有限公司',
# '成都康田农业开发有限公司',
# '中国电信股份有限公司德阳分公司',
# '成都市盛世捷利汽车销售有限公司',
# '四川醇机燃料科技有限公司崇州分公司',
# '成都荣广建材有限公司',
# '四川省阆中盛达经贸连锁有限公司老邻居超市营销分公司',
# '阆中市三鼎房地产开发有限公司',
# '南江县天益富硒农业科技有限公司',
# '广元放牛娃商贸有限公司',
# '崇州市浩云装饰有限公司',
# '崇州市妃子笑酒业有限公司',
# '成都金房物资贸易有限公司',
# '成都鹏宇园林有限公司',
# '渠县天通燃气有限公司',
# '崇州市众和通信设备有限公司',
# '成都市鸿途贸易有限公司',
# '成都锦和山水酒店管理有限公司崇州分公司',
# '红原县金佛旅游客运有限责任公司崇州汽车租赁分公司',
# '崇州市日益通物流有限责任公司',
# '成都市无茕世界家庭服务有限责任公司',
# '崇州西子广告传媒有限责任公司',
# '崇州立新建材有限公司',
# '崇州市众乐健康管理有限公司',
# '崇州建云德建材有限公司',
# '成都市龙程装饰有限公司',
# '崇州吉翔木业有限公司',
# '崇州汇赢天下金融服务外包有限公司',
# '崇州市广源中草药开发有限公司',
# '崇州麦点装饰工程有限公司',
# '崇州加发建材有限公司',
# '崇州市亚昌中草药开发有限公司',
# '四川龙泽实业有限公司',
# '温江霸力恒纤维板厂',
# '四川雷扬实业有限公司',
# '四川浩元恒达实业集团有限公司',
# '四川云龙公路桥梁建筑工程有限责任公司',
# '成都奥唐科技有限公司',
# '四川久大制盐有限责任公司',
# '成都飞达锦诚贸易有限公司',
# '成都亚青纸业有限公司',
# '四川恒瑞昌建筑工程有限公司',
# '四川多多生态农业有限公司',
# '四川鸿筑建筑劳务有限公司',
# '四川天罡木业制造有限责任公司',
# '攀枝花市嘉泰能源有限公司',
# '成都海昌置业有限公司']

# list_c = ['冰鉴科技']

list_c = ['内蒙古伊利实业集团股份有限公司',
          '广东温氏食品集团股份有限公司',
          '黑龙江农垦北大荒商贸集团有限责任公司',
          '新希望六和股份有限公司',
          '中粮屯河糖业股份有限公司',
          '临沂新程金锣肉制品集团有限公司',
          '内蒙古蒙牛乳业（集团）股份有限公司',
          '新希望集团有限公司',
          '北京顺鑫农业股份有限公司',
          '泉州福海粮油工业有限公司',
          '黑龙江象屿农业物产有限公司',
          '九三粮油工业集团有限公司',
            '内蒙古鄂尔多斯资源股份有限公司',
            '广东恒兴饲料实业股份有限公司',
            '山东新希望六和集团有限公司',
            '福建圣农发展股份有限公司',
            '金正大生态工程集团股份有限公司',
            '梅花生物科技集团股份有限公司',
            '菱花集团有限公司',
            '广东海大集团股份有限公司',
          '河南新野纺织股份有限公司',
          '黑龙江飞鹤乳业有限公司',
          '广东天禾农资股份有限公司',
          '贵州百灵企业集团制药股份有限公司',
          '广西凤糖生化股份有限公司',
            '黑龙江宾西牛业有限公司',
            '玉锋实业集团有限公司',
            '海南天然橡胶产业集团股份有限公司',
            '西霞口集团有限公司',
            '厦门中禾实业有限公司',
            '河北新发地农副产品有限公司',
            '獐子岛集团股份有限公司',
            '光明乳业股份有限公司',
            '湖南粮食集团有限责任公司',
            '石家庄君乐宝乳业有限公司',
            '辅仁药业集团有限公司',
            '宁夏伊品生物科技股份有限公司',
            '福建元成豆业有限公司',
            '济南圣泉集团股份有限公司',
            '中粮生物化学（安徽）股份有限公司',
            '浙江省粮油食品进出口股份有限公司',
            '山东富欣生物科技股份有限公司',
            '山东三维油脂集团股份有限公司',
            '浙江省农村发展集团有限公司',
            '青岛万福集团股份有限公司',
            '深圳市农产品股份有限公司',
            '天邦食品股份有限公司',
            '仲景宛西制药股份有限公司',
            '棕榈生态城镇发展股份有限公司',
            '唐人神集团股份有限公司',
            '金健米业股份有限公司',
            '湖州老恒和酿造有限公司',
            '河南众品食业股份有限公司',
            '冠县瑞祥生物科技开发有限公司',
            '辽宁禾丰牧业股份有限公司',
            '云南农垦集团有限责任公司',
            '黑龙江省完达山乳业股份有限公司',
            '临沂山松生物制品有限公司',
            '郑州思念食品有限公司',
            '北大荒丰缘集团有限公司',
            '牧原食品股份有限公司',
            '山东龙力生物科技股份有限公司',
            '维维食品饮料股份有限公司',
            '山东鲁丰集团有限公司',
            '鑫缘茧丝绸集团股份有限公司',
            '吉林吉春制药股份有限公司',
            '亚宝药业集团股份有限公司',
            '大湖水殖股份有限公司',
            '湖南湘佳牧业股份有限公司',
            '兖州市绿源食品有限公司',
            '河南省淇县永达食业有限公司',
            '现代牧业（集团）有限公司',
            '煌上煌集团有限公司',
            '内蒙古塞飞亚农业科技发展股份有限公司',
            '福建达利食品集团有限公司',
            '北京大北农科技集团股份有限公司',
            '浙江华统肉制品股份有限公司'
          ]
for company_name in list_c :
    app.send_task('ics.task.gsxt.cdrcb.task_wy.init', [company_name], queue='hezhen_test_queue', priority=0)

# for l in list_c:
#     app.send_task('ics.task.baidu_news_tasks.fetch', [l])

# from ics.scheduler import app
# r = app.send_task('ics.task.baidu_news_tasks.fetch', ['冰鉴'])
#
# print r.status
# print r.result
# print r.backend.get_result(r.task_id)

#
# import time
# time.sleep(5)
# print r.status
# print r.result


# app.send_task('ics.task.ex_tasks.add', [3, 7])


# from ics.scheduler import app
# for i in range(0, 1000):
#     app.send_task('ics.task.ex_tasks.add', [3, 7])
#     app.send_task('ics.task.ex_tasks.multi', [3, 7])

#
# from ics.task.ex_tasks import add
#
# for i in range(0,10):
#     r = add.delay(3,3)
#     print r.get()

# for i in range(0, 100):
#     app.send_task('ics.task.ex_tasks.add', args=(3,7),
#                           routing_key='add_queue')

# for i in range(0, 100):
#     app.send_task('ics.task.ex_tasks.add', args=(3,7),
#                       queue='multi_queue')
