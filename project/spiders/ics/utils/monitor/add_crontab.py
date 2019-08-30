#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:add_crontab.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/4
"""

import os
import sys


def add_cron_task(cron_str):
    """
    when linux system add new crontab task
    :return:
    """
    if os.path.exists('/var/spool/cron'):
        print('try to add new crontab task')
        with open('/var/spool/cron/root', 'r') as fr:
            curr_cont = fr.read()
        if cron_str not in curr_cont:
            curr_cont = cron_str + '\n' + curr_cont
            with open('/var/spool/cron/root', 'w') as fw:
                fw.write(curr_cont)
            print('add new crontab task success')
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == '__main__':
    cron_str = sys.argv[1]
    add_cron_task(cron_str)
