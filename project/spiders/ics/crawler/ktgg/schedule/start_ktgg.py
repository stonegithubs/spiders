# coding=utf-8


__author__ = 'wuyong'

import os
import sys
import json
import traceback
from apscheduler.schedulers.blocking import BlockingScheduler

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(BASE_DIR)

from ics.crawler.ktgg.core.constant import TASK_STATUS, KTGG_MANAGER_TABLE, KTGG_STATUS_TABLE, KTGG_TASK_QUEUE
from ics.scheduler import app
from ics.settings import default_settings
from ics.utils import get_ics_logger
from ics.utils.db.mysql_util import KtggMysqlDb
from ics.utils.exception_util import LogicException

logger = get_ics_logger('send_ktgg_task')

cycle_mapping = {  # 每早8点
    "every_day": {
        "trigger": 'cron',
        "day": "*",
        "hour": "8",
        "minute": "0",
        "second": "0",
    },
    "every_month": {  # 每月1号
        "trigger": 'cron',
        "day": "1",
        "month": "*",
        "hour": "8",
        "minute": "0",
        "second": "0"
    },
    "every_week": {  # 每周一早8点
        "trigger": 'cron',
        "day_of_week": "mon",
        "hour": "8",
        "minute": "0",
        "second": "0"
    },
    "every_season": {
        "trigger": "cron",
        "day": "1",
        "month": "*/3",
        "hour": "8",
        "minute": "0",
        "second": "0"
    },
    "every_half_second": {
        "trigger": 'cron',
        "second": "*/30"
    },
}


def immediate_start():
    mysql_db = KtggMysqlDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    select_sql = 'SELECT  a.ename, a.extra_args, b.id, b.crawl_date FROM {} as a,{} as b WHERE a.ename=b.ename AND b.state="{}";'.format(
        KTGG_MANAGER_TABLE, KTGG_STATUS_TABLE, TASK_STATUS.DISPATCH)

    result = mysql_db.query(select_sql)
    err_dict = None
    for ename, extra_args, a_id, crawl_date in result:
        try:
            if not extra_args:
                err_msg = u'临时启动参数为空，不合法，extra_args: {}'.format(extra_args)
                logger.error(err_msg)
                raise LogicException(err_msg)
            extra_dict = json.loads(extra_args)
            is_increment = extra_dict.get('is_increment')
            page = int(extra_dict['page'])
            if page < 1:
                err_msg = u'临时启动参数页码不合法： {}'.format(page)
                logger.error(err_msg)
                raise Exception(err_msg)
            args_dict = {'ename': ename, 'is_increment': is_increment, 'page': page}
            err_dict = args_dict
            app.send_task('ics.task.ktgg.{}.task.start'.format(ename), [args_dict],
                          queue=KTGG_TASK_QUEUE, priority=0)
            update_sql = 'UPDATE {} SET state={} WHERE id = "{}";'. \
                format(KTGG_STATUS_TABLE, TASK_STATUS.PREPARE, a_id)
            mysql_db.execSql(update_sql)
            logger.info(
                u'分配开庭公告立即启动任务成功, ename: {}, crawl_date: {}, args_dict: {}'.format(ename, crawl_date, args_dict))
        except Exception:
            logger.error(
                u'分配开庭公告立即启动任务失败：ename: {}，crawl_date:{}, err_dict:{}, 原因：{}'.format(ename, crawl_date, err_dict, traceback.format_exc()))


def start_task_by_cycle(cycle_type):
    select_sql = 'SELECT ename, is_increment, page FROM tbl_ktgg_manager WHERE cycle_type="{}";'.format(cycle_type)
    mysql_db = KtggMysqlDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    result = mysql_db.query(select_sql)

    if not result:
        logger.info(u'没有相关开庭公告任务， cycle_type:{}'.format(cycle_type))
        return
    for ename, is_increment, page in result:
        try:
            args_dict = {'ename': ename, 'is_increment': is_increment, 'page': page}
            app.send_task('ics.task.ktgg.{}.task.start'.format(ename), [args_dict],
                          queue=KTGG_TASK_QUEUE, priority=0)
        except Exception:
            logger.warning(
                u'分配开庭公告任务失败：ename: {}，cycle_type：{}， 原因：{}'.format(ename, cycle_type, traceback.format_exc()))
    logger.info(u'定时程序分配开庭公告任务完成，cycle_type: {}, 爬虫列表: {}'.format(cycle_type, result))


def main():
    timer_config = {
        "max_instances": 1,
        "execute_thread_max_num": 30
    }
    logger.info(u'开始启动定时调度主程序')
    sche = BlockingScheduler({
        'logger': logger,
        'apscheduler.timezone': 'Asia/Shanghai',
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': timer_config["execute_thread_max_num"],
        },
        "apscheduler.misfire_grace_time": "60",
        "apscheduler.job_defaults.max_instances": timer_config["max_instances"],
        'apscheduler.job_defaults.coalesce': 'false',
    })
    for k, v_dict in cycle_mapping.items():
        v_dict['id'] = k
        kwargs = {
            'cycle_type': k
        }
        v_dict['kwargs'] = kwargs
        logger.info(u'启动定时程序类型：{}'.format(k))
        sche.add_job(start_task_by_cycle, **v_dict)

    immediate_start_cycle = {
        "trigger": 'cron',
        "second": "*/2"
    }
    logger.info(u'启动定时程序类型：{}'.format('immediate_start'))
    sche.add_job(immediate_start, **immediate_start_cycle)
    sche.start()


if __name__ == '__main__':
    main()
