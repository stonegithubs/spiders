#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from kombu import Queue, Exchange
from ics.settings import default_settings

# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# 指定 task.add 任务 每 10s 跑一次, 任务参数为 (16,16)
# from datetime import timedelta
# CELERYBEAT_SCHEDULE = {
#     'add': {
#         'task': 'proj.task.add',
#         'schedule': timedelta(seconds=10),
#         'args': (16, 16)
#     }
# }

# crontab 风格
# from celery.schedules import crontab
# CELERYBEAT_SCHEDULE = {
#     "add": {
#         "task": "task.add",
#         "schedule": crontab(hour="*/3", minute=12),
#         "args": (16, 16),
#     }
# }

# 启动 Beat 程序
# $ celery beat -A proj

# 之后启动 worker 进程.
# $ celery -A proj worker -l info
#
# 或者
# $ celery -B -A proj worker -l info

CELERYD_POOL_RESTARTS = 'ENABLED'

# Broker 地址
# BROKER_URL = 'redis://120.26.101.244:6379/0'
# BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = default_settings.BROKER_URL

# 结果存储地址
CELERY_RESULT_BACKEND = default_settings.CELERY_RESULT_BACKEND
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'amqp://guest:guest@120.26.101.244:5672//'


# 任务序列化方式
CELERY_TASK_SERIALIZER = 'json'

# 任务执行结果序列化方式
CELERY_RESULT_SERIALIZER = 'json'

# 指定任务接受的内容类型(序列化)
CELERY_ACCEPT_CONTENT = ['json']

# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'


# import
CELERY_IMPORTS = default_settings.CELERY_IMPORTS

# celery任务执行结果的超时时间
CELERY_TASK_RESULT_EXPIRES = 60 * 60

# 可以让你的Celery更加可靠，只有当worker执行完任务后，才会告诉MQ，消息被消费。
# 另外根据资料，需要设置为True才能实现优先级，但优先级并未生效--实现失败
CELERY_ACKS_LATE = True
# CELERY_TASK_ACKS_LATE = True

# celery worker的并发数 也是命令行-c指定的数目,事实上实践发现并不是worker也多越好,保证任务不堆积,加上一定新增任务的预留就可以
# 另外根据资料，需要设置为1才能实现优先级，但优先级并未生效--实现失败
CELERYD_CONCURRENCY = 4

# celery worker 每次去rabbitmq取任务的数量，我这里预取了5个慢慢执行,因为任务有长有短没有预取太多
CELERYD_PREFETCH_MULTIPLIER = 1

# 每个worker执行了多少任务就会死掉，我建议数量可以大一些，比如200 【避免内存泄露】
CELERYD_MAX_TASKS_PER_CHILD = 50

# 配合act_late参数，在task经过超时时间之后如果还没被ack, 就会被发送到其他worker去执行(查了文档 貌似只支持redis和sqs)
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60}

# 任务超时时间，超过这个时间的话，就先生成新的进程，并通过信号将hanging的进程杀死
# CELERYD_TASK_TIME_LIMIT = 500

CELERYD_TASK_SOFT_TIME_LIMIT = default_settings.CELERYD_TASK_SOFT_TIME_LIMIT

# 默认的队列
CELERY_DEFAULT_QUEUE = "default_queue"

CELERY_ENABLE_UTC = False

# https://github.com/celery/celery/issues/4226 Broken Pipe 问题
BROKER_POOL_LIMIT = None

# 定义任务队列.
# (当使用Redis作为broker时，Exchange 的名字必须和 Queue 的名字一样)（此处不知道有无必要进行申明，因为woker启动时会自动生成队列，这里的队列申明无效）
# CELERY_QUEUES = (
#     # 路由键 以 "default." 开头的消息都进入 default 队列.
#     # Queue('default', routing_key="default.#"),
#     # 路由键 以 "add." 开头的消息都进入 add 队列.
#     # Queue('add', routing_key="add.#"),
#     # 路由键 以 "multi." 开头的消息都进入 multi 队列.
#     # Queue('multi', routing_key="multi.#"),
#
#     Queue('default_queue', Exchange('default_queue'), routing_key="default_queue"),
#     Queue('tuliu_queue', Exchange('tuliu_queue'), routing_key="tuliu_queue", consumer_arguments={'x-priority': 22}),
#     # 数字越大，优先级越高
#     Queue('pipe_queue', Exchange('pipe_queue'), routing_key="pipe_queue", consumer_arguments={'x-priority': 88}),
#     Queue('test_queue', Exchange('test_queue'), routing_key="test_queue"),
#     Queue('baidu_news_queue', Exchange('baidu_news_queue'), routing_key="baidu_news_queue"),
#
#     # https://github.com/celery/celery/issues/2635 测试了优先级的实现方式，发现并未生效！未找到原因(2018-06-6) 找到原因）
#     Queue('priority', Exchange('priority'), routing_key="priority", queue_arguments={'x-max-priority': 10})
#
#     # Queue('priority_1', routing_key="priority_1", consumer_arguments={'x-priority': 1}),
#     # Queue('priority_2', routing_key="priority_0", consumer_arguments={'x-priority': 2})
# )


# CELERY_ROUTES = {
#     'ics.task.core.common_task.download_request': {
#         'queue': 'download_queue'
#     },
#     'ics.task.core.pipe_task.to_console': {
#         'queue': 'pipe_queue'
#     },
#     'ics.task.core.pipe_task.to_mysql': {
#         'queue': 'pipe_queue'
#     },
#     'ics.task.core.pipe_task.download_pic': {
#         'queue': 'pipe_queue'
#     }
# }
