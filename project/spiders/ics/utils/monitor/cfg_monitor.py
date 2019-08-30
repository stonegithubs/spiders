#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:send_email.py
description:
author:crazy_jacky
version: 1.0
date:2018/8/9
"""
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from ics.utils import get_ics_logger
from ics.utils.email.ics_email import Send_Email
from ics.utils.monitor.cfg.get_config import read_config

reload(sys)

sys.setdefaultencoding('utf-8')

logger = get_ics_logger(__name__)


def update_crontab():
    cfg_dic = read_config()
    c_file_path = os.path.join(os.path.dirname(__file__), 'add_crontab.py')
    msg_lst = []
    theme = cfg_dic['monitor'][0]['theme']
    for key in cfg_dic:
        check_fq = cfg_dic[key][0].get('check_fq')
        if check_fq:
            logger.info('begin to add crontab task: {}'.format(check_fq))
            res = os.system('sudo python {} "{}"'.format(c_file_path, check_fq))
            if res:
                msg_lst.append(check_fq)
    return theme, msg_lst


if __name__ == '__main__':
    theme, msg_lst = update_crontab()
    if msg_lst:
        ss = Send_Email(theme)
        data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg = '新增crontab定时任务详细信息如下：\n' + '\n'.join(msg_lst) + '\n' + data_time
        ss.send_mail(msg)
