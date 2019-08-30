#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.utils.rabbit_mq import RabbitMq
from ics.settings import default_settings
import uuid

mq = RabbitMq('guest', 'guest', '47.99.51.210', 5672)
for i in range(10):

    json_str = '{"task_name":"zhixing","task_id":"%s","target_name":"刘抗山","target_id": "","target_type":0,"search_type":"QWJS","search_param":"（2013）民申字第1507号"}' % str(
        uuid.uuid4())

    # json_str = '{"task_name":"zhixing","task_id":"%s","target_name":"刘东","target_id": "","target_type":0}' % str(
    # json_str = '{"task_name":"zgcpws","task_id":"%s","target_name":"刘东","target_id": "","target_type":0,"search_type":"AH","search_param":"（2013）民申字第1507号"}' % str(
    #     uuid.uuid4())

    json_str = '{"task_name":"zhixing","task_id":"%s","target_name":"刘东","target_id": "","target_type":0}' % str(
        uuid.uuid4())

    # json_str = '{"task_name":"zgcpws","task_id":"%s","target_name":"刘抗山","target_id": "","target_type":0,"search_type":"DSR","search_param":"刘建东"}' % str(uuid.uuid4())

    mq.send_msg(default_settings.CDRCB_NORMAL_PUSH_QUEUE, json_str)

# json_str = '{"task_name":"zhixing","task_id":"%s","target_name":"刘可痈","target_id": "","target_type":0}' % str(uuid.uuid4())
#
# # json_str = '{"task_name":"zgcpws","task_id":"%s","target_name":"刘抗山","target_id": "","target_type":0,"search_type":"DSR","search_param":"刘建东"}' % str(uuid.uuid4())
#
# mq.send_msg(default_settings.CDRCB_NORMAL_PUSH_QUEUE,json_str)

############################################
