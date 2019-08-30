#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import pika


def send_message(queue_neme, body):
    username = 'guest'  # 指定远程rabbitmq的用户名密码
    pwd = 'guest'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(pika.ConnectionParameters('120.26.101.244', credentials=user_pwd))  # 创建连接
    chan = s_conn.channel()  # 在连接上创建一个频道

    chan.queue_declare(queue=queue_neme, durable=True)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

    chan.basic_publish(
        exchange='',  # 交换机
        routing_key=queue_neme,  # 路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
        body=body,
        properties=pika.BasicProperties(delivery_mode=2, )  # 设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
    )  # 生产者要发送的消息

    print("[producer] send '%s" % body)

    s_conn.close()  # 当生产者发送完消息后，可选择关闭连接
