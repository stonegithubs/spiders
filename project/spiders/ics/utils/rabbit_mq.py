# coding=utf-8

__author__ = 'wu_yong'


import json
import pika
from ics.utils.singleton import Singleton


class RabbitMq(Singleton):

    def __init__(self, username, password, host, port=5672, logger=None):
        self.logger = logger
        self.user_pwd = pika.PlainCredentials(username, password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host, port, credentials=self.user_pwd))
        self.channel = self.conn.channel()

    def send_msg(self, queue_name, body, properties=None, exchange=''):
        """
        生产消息
        :return:
        """
        send_body = json.dumps(body, ensure_ascii=False) if isinstance(body, (dict, list)) else body
        properties = properties or pika.BasicProperties(delivery_mode=2)
        properties.content_type= 'application/json'
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange=exchange,          # 交换机
            routing_key=queue_name,     # 路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
            body=send_body,
            properties=properties,      # 设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
        )
        if self.logger:
            self.logger.info(u'消息发送成功, queue_name: {}，msg: {}'.format(queue_name, send_body))

    def consume_msg(self, queue_name, callback):
        """
        消费消息
        :return:
        """
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)    # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息
        self.channel.basic_consume(
            callback,                               # 调用回调函数，从队列里取消息
            queue=queue_name                        # 指定取消息的队列名
        )
        if self.logger:
            self.logger.info(u'开始循环消费消息， queue_name :{}'.format(queue_name))
        self.channel.start_consuming()

    def __del__(self):
        print ('---end---')
        self.conn.close()


