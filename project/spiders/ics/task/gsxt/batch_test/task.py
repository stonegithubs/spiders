#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wu_yong'

import sys
from ics.task.gsxt.batch_test.task_logic import *
from ics.scheduler import app
from ics.scheduler.new_task import StableTask
from ics.task.gsxt.batch_test.constant import *
from ics.utils.decorator import stable2
from ics.utils.exception_util import LogicException, DownloaderException

reload(sys)
sys.setdefaultencoding('utf-8')


@app.task(bind=True, base=StableTask, rate_limit='120/m', ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def start(self, seed_dict):
    logger.info(u'开始了:{}'.format(seed_dict))
    if seed_dict.get('target_name'):
        seed_dict['company_key'] = seed_dict['target_name']
    elif seed_dict.get('target_id'):
        seed_dict['company_key'] = seed_dict['target_id']
    else:
        logger.error(u'输入种子不合法，不包含搜索关键字')
        return
    value_dict['seed_dict'] = seed_dict
    page_dict['seed_dict'] = seed_dict
    logger.info(u'开始了value_dict:{}'.format(value_dict))
    logger.info(u'开始抓取种子: {}'.format(seed_dict))
    init_home()
    get_validate()
    init_search_list()
    iter_search_list()

    pass


if __name__ == '__main__':
    seed_dict = {
        "task_name": "gsxt",
        "task_id": str(uuid.uuid4()),
        "target_name": u"辅仁药业集团有限公司",  # 四川众和源餐饮管理有限公司
        "target_id": "",
        "target_type": 1,
        "company_key": u"辅仁药业集团有限公司",
    }

    start(seed_dict)

