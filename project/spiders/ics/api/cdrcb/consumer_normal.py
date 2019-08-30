#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import pika
from ics.scheduler import app
import json
import traceback
from ics.settings import default_settings
import datetime

def get_now():
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
    return nowTime

username = default_settings.RABBIT_MQ_USERNAME
pwd = default_settings.RABBIT_MQ_PASSWORD
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(
    pika.ConnectionParameters(default_settings.RABBIT_MQ_HOST, credentials=user_pwd))  # 创建连接
chan = s_conn.channel()  # 在连接上创建一个频道

chan.queue_declare(queue=default_settings.CDRCB_NORMAL_PUSH_QUEUE,
                   durable=True)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行,设置队列持久化，注意不要跟已存在的队列重名，否则有报错


def callback(ch, method, properties, body):  # 定义一个回调函数，用来接收生产者发送的消息
    try:
        print("[%s][消费者] recv %s" % (get_now(),body))
        task = json.loads(body)
        app.send_task('ics.task.' + task['task_name'] + '.cdrcb.task.start', [task],
                      queue='queue_cdrcb_normal_' + task['task_name'] + default_settings.CDRCB_PROJECT_SUFFIX.lower(),
                      priority=0)
        print("[%s]send task success" % get_now())
    except Exception:
        print ('[%s]body:' % get_now()) + body + '\r\n' + traceback.format_exc()

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 接收到消息后会给rabbitmq发送一个确认


chan.basic_qos(prefetch_count=1)  # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息

chan.basic_consume(
    callback,  # 调用回调函数，从队列里取消息
    queue=default_settings.CDRCB_NORMAL_PUSH_QUEUE  # 指定取消息的队列名
    # no_ack=True
)  # 取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可

print('[%s][消费者] waiting for msg .' % get_now())

chan.start_consuming()  # 开始循环取消息
