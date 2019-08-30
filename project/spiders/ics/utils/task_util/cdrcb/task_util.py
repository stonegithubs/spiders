#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wu_yong'

from datetime import datetime
from ics.utils.rabbit_mq import RabbitMq
from ics.settings import default_settings
from ics.utils.db import CdrcbDb
from ics.utils.duplicate.bloom_filter import BloomFilter

bloom_filter = BloomFilter(db=default_settings.REDIS_BLOOM_FILTER_DB)


class TASK_STATUS(object):
    """
    任务状态
    """
    SUCCESS = 'success'
    FAILED = 'fail'
    NULL = 'null'


def send_no_record(seed_dict=None, logger=None, table_name=None):
    """
    网页上没有记录
    :param seed_dict:
    :param logger:
    :param table_name:
    :return:
    """
    rabbit_db = RabbitMq(
        default_settings.RABBIT_MQ_USERNAME,
        default_settings.RABBIT_MQ_PASSWORD,
        default_settings.RABBIT_MQ_HOST,
        default_settings.RABBIT_MQ_PORT,
        logger=logger)
    task_id = seed_dict['task_id']
    table_name = table_name
    result_queue_name = default_settings.CDRCB_NORMAL_RESULT_QUEUE
    send_dict = {
        "task_id": task_id,
        "task_status": TASK_STATUS.NULL,
        "error_msg": u'网页无数据',
        "tbl_name": table_name,
        "total_cnt": 0,
        "real_success_cnt": 0,
    }
    logger.info(u'任务task_id:{}抓取完成，抓取量:{}，抓取成功量:{}，总量:{}, 开始发送msg到队列{}'.format(task_id, 0, 0, 0, result_queue_name))
    rabbit_db.send_msg(result_queue_name, send_dict)


def insert_mysql(table, model, logger):
    mysql_db = CdrcbDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    # logger.info('mysql_db_id: {}'.format(mysql_db))
    mysql_db.insert_dic(table, model)


def add_common_key(etl_dict, seed_dict, **kwargs):
    """
    source_id = None, page_source = None, total_cnt = None, err_msg = None, status = None
    :param etl_dict:
    :param seed_dict:
    :param kwargs:
    :return:
    """
    etl_dict['task_id'] = seed_dict.get('task_id')
    etl_dict['target_name'] = seed_dict.get('target_name')
    etl_dict['target_id'] = seed_dict.get('target_id')
    etl_dict['target_type'] = seed_dict.get('target_type')
    etl_dict['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    etl_dict['source_id'] = kwargs.get('source_id', '')
    etl_dict['page_source'] = kwargs.get('page_source', '')
    etl_dict['error_msg'] = kwargs.get('err_msg', '')
    etl_dict['status'] = kwargs.get('status', '')
    etl_dict['total_cnt'] = kwargs.get('total_cnt', -1)


def search_error_callback(callback_params, excption_msg=''):
    """
    用于非列表页和详情页的error_back
    :param callback_params:
    :param excption_msg:
    :return:
    """

    seed_dict = callback_params.get('seed_dict')
    logger = callback_params.get('logger')
    tbl_name = callback_params.get('table_name')
    excption_msg = u'搜索失败,{}'.format(excption_msg)
    msg_dict = {
        "task_id": seed_dict['task_id'],
        "task_status": TASK_STATUS.FAILED,
        "error_msg": excption_msg,
        "tbl_name": tbl_name,
    }
    logger.info(u'任务task_id:{}抓取失败, 开始发送msg到队列{}'.format(seed_dict['task_id'], default_settings.CDRCB_NORMAL_RESULT_QUEUE))
    rabbit_db = RabbitMq(
        default_settings.RABBIT_MQ_USERNAME,
        default_settings.RABBIT_MQ_PASSWORD,
        default_settings.RABBIT_MQ_HOST,
        default_settings.RABBIT_MQ_PORT,
        logger=logger)
    rabbit_db.send_msg(default_settings.CDRCB_NORMAL_RESULT_QUEUE, msg_dict)
    logger.info(u'任务task_id:{}抓取失败, 发送msg到队列完成{}'.format(seed_dict['task_id'], default_settings.CDRCB_NORMAL_RESULT_QUEUE))


def error_callback(callback_params, excption_msg):
    etl_dict = {}
    seed_dict = callback_params['seed_dict']
    table_name = callback_params['table_name']
    logger = callback_params['logger']
    lose_cnt = callback_params['lose_cnt']
    add_common_key(etl_dict, seed_dict, err_msg=excption_msg, status=TASK_STATUS.FAILED)
    for i in range(lose_cnt):
        insert_mysql(table_name, etl_dict, logger)


def check_result_and_send_msg(table_name, total_cnt, task_id, logger,
                              err_msg=None):
    mysql_db = CdrcbDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    # logger.info('mysql_db_id: {}'.format(mysql_db))
    rabbit_db = RabbitMq(
        default_settings.RABBIT_MQ_USERNAME,
        default_settings.RABBIT_MQ_PASSWORD,
        default_settings.RABBIT_MQ_HOST,
        default_settings.RABBIT_MQ_PORT,
        logger=logger)
    total_query_sql = 'SELECT COUNT(*) FROM {} WHERE task_id="{}"'.format(table_name, task_id)
    real_total_cnt = mysql_db.query(total_query_sql)[0][0]
    if real_total_cnt == total_cnt:
        if bloom_filter.dup_filter(task_id):
            logger.info(u'已经发送消息，不再发送：' + task_id)
            return
        else:
            query_sql = "SELECT COUNT(*) FROM {} WHERE task_id='{}' AND status='{}'".format(table_name, task_id,
                                                                                            TASK_STATUS.SUCCESS)
            real_success_cnt = mysql_db.query(query_sql)[0][0]
            send_dict = {
                "task_id": task_id,
                "task_status": TASK_STATUS.SUCCESS,
                "error_msg": err_msg,
                "tbl_name": table_name,
                "total_cnt": total_cnt,
                "success_cnt": real_success_cnt,
            }
            if real_success_cnt != real_total_cnt:
                send_dict['task_status'] = TASK_STATUS.FAILED
                send_dict['error_msg'] = err_msg or u'抓取数据有丢失'
            infos = u'任务task_id:{}抓取完成，抓取量{}，抓取成功量{}，总量{}, 开始发送msg到队列{}'
            logger.info(
                infos.format(task_id, real_total_cnt, real_success_cnt, total_cnt, default_settings.CDRCB_NORMAL_RESULT_QUEUE))
            rabbit_db.send_msg(default_settings.CDRCB_NORMAL_RESULT_QUEUE, send_dict)
    else:
        logger.info(u'任务task_id:{} 抓取量为：{}, 总量为: {}'.format(task_id, real_total_cnt, total_cnt))


def get_current_page_cnt(total_cnt, per_page, current_page):
    """
    计算翻页时，具体页码的数据条数
    :param total_cnt:
    :param per_page:
    :param current_page:
    :return:
    """
    total_page = (total_cnt - 1) / per_page + 1
    last_page_cnt = total_cnt % per_page
    if current_page == total_page:
        return last_page_cnt
    else:
        return per_page


def update_seed_to_no_reord(task_id, logger):
    NO_RECORD = 107
    try:
        mysql_db = CdrcbDb(default_settings.MYSQL_TASK_DATA_DB, logger)
        logger.info(u'开始更新种子状态，task_id:{}'.format(task_id))
        update_pattern = 'UPDATE seeds SET status={} WHERE task_id = "{}";'.format(NO_RECORD, task_id)
        mysql_db.execSql(update_pattern)
        logger.info(u'更新种子状态完成，task_id:{}'.format(task_id))
    except Exception as e:
        logger.error(u'更新种子状态异常：{}'.format(str(e)))


if __name__ == '__main__':
    get_current_page_cnt(99, 10, 1)