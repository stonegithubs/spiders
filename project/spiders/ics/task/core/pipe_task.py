#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.scheduler import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def to_console(item):
    logger.info('-----------------console info:' + item['name'])


def send_to_console(item, queue):
    app.send_task('ics.task.core.pipe_task.to_console', [item], queue=queue)


@app.task
def to_mysql(item):
    logger.info('-----------------download info to mysql success ...-----------------')


def send_to_mysql(item, queue):
    app.send_task('ics.task.core.pipe_task.to_mysql', [item], queue=queue)


@app.task
def download_pic(item):
    logger.info('-----------------download pic success ...-----------------')


def send_to_download_pic(item, queue):
    app.send_task('ics.task.core.pipe_task.download_pic', [item], queue=queue)
