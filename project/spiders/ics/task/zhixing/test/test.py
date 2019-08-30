# coding=utf-8
import traceback

from utils.rabbit_mq import RabbitMq
from task.zhixing.cdrcb.mysql_pool import mysql_pool
from retry import retry

from utils import get_ics_logger

logger = get_ics_logger('test_check_result_is_ok')


@retry(exceptions=RuntimeError, tries=3, delay=1, logger=logger)
def insert_mysql(table, model):
    db = mysql_pool.connection()
    cursor = db.cursor()
    qmarks = ', '.join(['%s'] * len(model))  # 用于替换记录值
    cols = ', '.join(model.keys())  # 字段名
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
    logger.info(u'开始保存数据，table：{}'.format(table))
    try:
        res = cursor.execute(sql, model.values())
        db.commit()
        logger.info(u'保存数据成功，table：{}'.format(table))
        return res
    except Exception:
        db.rollback()
        db.close()
        logger.info(u'保存数据失败，table：{}, 原因: {}, sql: {}'.format(table, traceback.format_exc(), sql))
        raise RuntimeError('mysql error')
    db.close()


# def query(sql):
#     """
#         执行查询语句
#     """
#     db = mysql_pool.connection()
#     cursor = db.cursor()
#     # cur = cursor.cursor()
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     return result
#
#
# def update(sql):
#     db = mysql_pool.connection()
#     cursor = db.cursor()
#     # cur = cursor.cursor()
#     cursor.execute(sql)
#     db.commit()
#     result = cursor.fetchall()
#     return result
#
# def select_from_mysql(sql):
#     db = mysql_pool.connection()
#     cursor = db.cursor()

TABLE_NAME = 'zhixing_data'
RESULT_QUEUE_NAME = 'result_queue_name'


class TASK_STATUS(object):
    SUCCESS = 'success'
    FAILED = 'failed'


ins = RabbitMq(TEST_RABBIT_MQ['username'],
               TEST_RABBIT_MQ['password'],
               TEST_RABBIT_MQ['host'],
               TEST_RABBIT_MQ['port'],
               logger=logger)


def check_result_and_send_msg(mysql_db, rbbit_client, total_cnt, task_id, target_status):
    """
    用于检测某任务id,抓取到的数量是否达标
    如果错误，更新错误日志，新增记录,抓取状态,
    如果达标，更新抓取状态为success
    {
        "task_id" : "b46aacfc-9887-4a5b-9d15-ad2c30df5109",
        "task_status" : "suceess",
        "error_msg" : "",
        "tbl_name" : "tbl_cpws",
        "total_cnt":"",
        "real_cnt":"",
    }
    :return:
    """
    from ics.utils.db import CdrcbDb
    dbs = CdrcbDb('zhixing_test')

    query_sql = "SELECT COUNT(*) FROM {} WHERE task_id={}".format(TABLE_NAME, task_id)
    real_cnt = mysql_db.query(query_sql)[0][0]
    if real_cnt == total_cnt:
        success_sql = "UPDATE {} SET status='{}' WHERE task_id={}".format(TABLE_NAME, target_status, task_id)
        mysql_db.execSql(success_sql)
        send_dict = {
            "task_id": task_id,
            "task_status": target_status,
            "error_msg": "",
            "tbl_name": TABLE_NAME,
            "total_cnt": total_cnt,
            "real_cnt": real_cnt,
        }
        rbbit_client.produce_msg(RESULT_QUEUE_NAME, send_dict)

    else:
        print ('crawler_cnt is {}'.format(real_cnt))





# def test(db):
#     sql = "update {} set status='{}' where task_id={}".format(table, SUCCESS, 110)
#     db.execSql(sql)
#



if __name__ == '__main__':
    # a = {'a':1, 'b':2, 'c':3}
    s = '%s, %s, %s'
    print s%tuple([1,2,3])
    #
    # cols = ', '.join(query_dict.keys())  # 字段名
    # # sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, query_dict)
    #
    # sql = "SELECT COUNT(*) FROM zhixing_data WHERE task_id=1101"
    # res = query(sql)
    # if res[0][0] == total_cnt:
    #     # 更新数据库状态
    #     # 下发信息到rabbitmq
    #     pass
    # else:
    #     print ('count: {}'.format(res[0][0]))
    # print res
    # test_check_result_is_ok(total_cnt)