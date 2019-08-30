#coding=utf-8
from settings.default_settings import RABBIT_MQ
from utils.rabbit_mq import RabbitMq
from ics.utils import get_ics_logger


def send_zhixing_seed_msg(queue_name, data):
    logger = get_ics_logger('RABBIT_MQ')
    ins = RabbitMq(RABBIT_MQ['username'],
                   RABBIT_MQ['password'],
                   RABBIT_MQ['host'],
                   RABBIT_MQ['port'],
                   logger=logger)

    for i in range(10):
        data['task_id'] = str(i)
        ins.produce_msg(queue_name, data)


if __name__ == '__main__':
    queue_name = 'zhixing_queue_01'
    # celery worker -E -Q zhixing_queue_01 -n test.%h -l info --app ics --pool=solo
    data = {
        "task_name": "zhixing",
        "task_id": "b46aacfc-9887-4a5b-9d15-ad2c30df5109",
        "target_name": "张三",# name
        "target_id": "",  # card_id
        "target_type": 0  # 个人0/企业1
    }

    send_zhixing_seed_msg(queue_name, data)
