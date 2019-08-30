#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import pika
from ics.scheduler import app
import json
import traceback

username = 'guest'  # 指定远程rabbitmq的用户名密码
pwd = 'guest'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('120.26.101.244', credentials=user_pwd))  # 创建连接
chan = s_conn.channel()  # 在连接上创建一个频道

chan.queue_declare(queue='queue_api',
                   durable=True)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行,设置队列持久化，注意不要跟已存在的队列重名，否则有报错


def callback(ch, method, properties, body):  # 定义一个回调函数，用来接收生产者发送的消息
    try:
        print("[消费者] recv %s" % body)
        task = json.loads(body)
        app.send_task(task['task_name'], eval(task['args']), queue=task['queue'], priority=task['priority'])
        print("send task success")
    except Exception:
        print 'body:' + body + '\r\n' + traceback.format_exc()

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 接收到消息后会给rabbitmq发送一个确认


chan.basic_qos(prefetch_count=1)  # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息

chan.basic_consume(
    callback,  # 调用回调函数，从队列里取消息
    queue='queue_api'  # 指定取消息的队列名
    # no_ack=True
)  # 取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可

print('[消费者] waiting for msg .')
chan.start_consuming()  # 开始循环取消息
