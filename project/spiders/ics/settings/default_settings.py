#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


LOG_DIR = '/data/logs'
####################################################################################

REDIS_BLOOM_FILTER_DB = 8  # bloomfilter 所用db

REDIS_LOCK_DB = 2  # redislocker 所用db

REDIS_CELERY_BACKEND_DB = 0  # celery backend 所用db

REDIS_PROXY_DLY = 7  # 代理云 所用db

#####################################################################################

BROKER_URL = 'amqp://guest:guest@47.99.51.210:5672//'

CELERY_RESULT_BACKEND = 'redis://:icekredit@47.99.51.210:6379/' + str(REDIS_CELERY_BACKEND_DB)

MYSQL_HOST = 'rm-bp11towre3n815e78o.mysql.rds.aliyuncs.com'

MYSQL_PORT = 3306

MYSQL_USERNAME = 'gouchao'

MYSQL_PASSWORD = 'Gouchao!2018'

MYSQL_TASK_DATA_DB = 'cdrcb_crawl'

PROXY_3HOUR = 'http://webapi.http.zhimacangku.com/getip?num=%s&type=2&pro=0&city=0&yys=100017&port=1&pack=25680&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions='

# PROXY_25MIN = 'http://webapi.http.zhimacangku.com/getip?num=%s&type=2&pro=0&city=0&yys=100017&port=1&pack=25678&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions='

PROXY_25MIN = 'http://webapi.http.zhimacangku.com/getip?num=%s&type=2&pro=0&city=0&yys=100017&port=1&pack=27259&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions='

PROXY_25MIN_TEST = 'http://webapi.http.zhimacangku.com/getip?num=%s&type=2&pro=0&city=0&yys=100017&port=1&pack=28962&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions='

DLY_PROXY_URL = "http://dly.134t.com/query.txt?key=NPC7693F94&word=&count=1000&detail=true"

DLY_AUTH = "darkwings2018:maosu1989"

RABBIT_MQ_USERNAME = 'guest'

RABBIT_MQ_PASSWORD = 'guest'

RABBIT_MQ_HOST = '47.99.51.210'

RABBIT_MQ_PORT = '5672'

REDIS_HOST = '47.99.51.210'

REDIS_PORT = 6379

REDIS_PASSWORD = 'icekredit'

#####################################################################################

CDRCB_PROJECT_SUFFIX = '_TEST'

CDRCB_NORMAL_RESULT_QUEUE = 'CDRCB_NORMAL_RESULT_QUEUE' + CDRCB_PROJECT_SUFFIX  # 抓取结果的消息，需要发送到的队列

CDRCB_NORMAL_PUSH_QUEUE = 'CDRCB_NORMAL_PUSH_QUEUE' + CDRCB_PROJECT_SUFFIX  # 获取外部任务的消息队列

ZHIXING_NORMAL_TASK_QUEUE = 'queue_cdrcb_normal_zhixing' + CDRCB_PROJECT_SUFFIX.lower()  # 被执行人任务队列

ZGCPWS_NORMAL_TASK_QUEUE = 'queue_cdrcb_normal_zgcpws' + CDRCB_PROJECT_SUFFIX.lower()  # 中国裁判文书任务队列

ZGCPWS_APP_NORMAL_TASK_QUEUE = 'queue_cdrcb_normal_zgcpws_app' + CDRCB_PROJECT_SUFFIX.lower()  # 中国裁判文书app任务队列

SHIXIN_NORMAL_TASK_QUEUE = 'queue_cdrcb_normal_fysx' + CDRCB_PROJECT_SUFFIX.lower()  # 失信被执行人任务队列

ZHIXING_DATA_TABLE = 'tbl_zhixing'  # 被执行人数据库表

SHIXIN_DATA_TABLE = 'tbl_fysx'  # 失信被执行人数据库表

ZGCPWS_DATA_TABLE = 'tbl_zgcpws'  # 中国裁判文书数据库表

#####################################################################################

SAVE_CAPTCHA = True


#####################################################################################
# 超级鹰打码配置信息：
# CJY_USER = 'ice99cjy'
# CJY_PWD = 'icekredit'
# CJY_SOFT_ID = '13d4d205969cae0b5f81eafc7347286b'

CJY_USER = 'icekredit'
CJY_PWD = 'icekredit-cjy-2018!'
CJY_SOFT_ID = '014e62cafa998d26cf783d415eb5b307'

#####################################################################################
# 若快打码配置信息：
RK_USER = 'rk99ice'
RK_PWD = 'icekredit'
RK_SOFT_ID = '109933'
RK_KEY = '4e68e53b7e4a4487850e2f9df6982664'

####################################################################################
# 聚合打码
APPKEY = '6c33077d3febe09996af3d7f663d8b17'

#####################################################################################

STMP_SERVER = 'smtp.exmail.qq.com'
LOGIN_CODE = 'Zheng1989'
SEND_FROM = 'zheng_qipeng@icekredit.com'
SEND_TO = 'zheng_qipeng@icekredit.com;wu_yong@icekredit.com;he_zhen@icekredit.com;mao_jingwen@icekredit.com'
PROXY_URL = 'http://web.http.cnapi.cc/index/index/get_my_package_balance?neek=48328&appkey=8e5df8b49ea40dba70f40689af6316ea&ac=27259'
PROXY_WARN_CNT = 500
#####################################################################################

# 破解js的服务和客户端相关配置
JS_SERVER_URL = 'http://47.99.65.29:6666/execjs'
# JS_SERVER_URL = 'http://47.99.51.210:6666/execjs'
JS_SERVER_CHROME_PATH = '/opt/google/chrome/chromedriver'
JS_SERVER_AUTH_USERNAME = 'spider'
JS_SERVER_AUTH_PASSWORD = 'spider2018'

#####################################################################################


# BATCH_TEST_CONFIG 供测试环境使用

BATCH_TEST_SUFFIX = '_TEST'
# queue_batch_test_normal_zhixing_wuyong
BATCH_TEST_NORMAL_PUSH_QUEUE = 'BATCH_TEST_NORMAL_PUSH_QUEUE' + BATCH_TEST_SUFFIX  # 获取外部任务的消息队列

BATCH_TEST_ZHIXING_NORMAL_TASK_QUEUE = 'queue_batch_test_normal_zhixing' + BATCH_TEST_SUFFIX.lower()  # 被执行人任务队列

BATCH_TEST_ZGCPWS_NORMAL_TASK_QUEUE = 'queue_batch_test_normal_zgcpws' + BATCH_TEST_SUFFIX.lower()  # 中国裁判文书任务队列

BATCH_TEST_SHIXIN_NORMAL_TASK_QUEUE = 'queue_batch_test_normal_fysx' + BATCH_TEST_SUFFIX.lower()  # 失信被执行人任务队列


CELERY_IMPORTS = (
    'ics.task.zhixing.cdrcb.task',
    'ics.task.fysx.cdrcb.task',
    'ics.task.zgcpws.cdrcb.task',
    'ics.task.zgcpws_app.cdrcb.task',
)

#####################################################################################

ZGCPWS_DOC_ID_NORMAL_TASK_QUEUE = 'zgcpws_doc_id_task_queue'

ZGCPWS_BATCH_NORMAL_TASK_QUEUE = 'zgcpws_batch_task_queue'

CELERYD_TASK_SOFT_TIME_LIMIT = 120