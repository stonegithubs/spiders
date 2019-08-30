#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from celery import Celery

app = Celery('ics')

app.config_from_object('ics.config.config')

# app.conf.task_acks_late = True
# app.conf.broker_transport_options = {'visibility_timeout': 3}
# app.conf.task_time_limit = 3

# 若使用优先级，取消此注释
app.conf.task_queue_max_priority = 10
app.conf.task_reject_on_worker_lost = True
app.conf.worker_prefetch_multiplier = 1
app.conf.broker_pool_limit = 100

# app.conf.broker_transport_options = {'visibility_timeout': 60}
# app.conf.task_time_limit = 60

# celery worker -Q queuename 若没有Q参数，在worker启动时自动初始化所有队列
# from kombu import Exchange, Queue
# app.conf.task_queues = [
#     Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
#     Queue('default_queue', Exchange('default_queue'), routing_key="default_queue"),
#     Queue('tuliu_queue', Exchange('tuliu_queue'), routing_key="tuliu_queue", consumer_arguments={'x-priority': 22}),
#     Queue('pipe_queue', Exchange('pipe_queue'), routing_key="pipe_queue", consumer_arguments={'x-priority': 88}),
#     Queue('test_queue', Exchange('test_queue'), routing_key="test_queue"),
#     Queue('baidu_news_queue', Exchange('baidu_news_queue'), routing_key="baidu_news_queue")
# ]

# 重载配置
# app.conf.update(
#     task_queue_max_priority = 10
#     result_expires=3600,
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'],
#     CELERY_RESULT_SERIALIZER='json',
#     CELERYD_CONCURRENCY=1
# )
