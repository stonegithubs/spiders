#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wu_yong'


import os
import sys
import uuid
import time
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from celery.utils.log import get_task_logger

from ics.settings.default_settings import LOG_DIR


class ICSTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename.replace('.log', '') + "-" + time.strftime(self.suffix, timeTuple)
        # dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        # if os.path.exists(dfn):
        #     os.remove(dfn)

        # Issue 18940: A file may not have been created if delay is True.
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

        self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)

        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend

        self.rolloverAt = newRolloverAt


def get_custom_task_logger(log_name, level='INFO', logfile_name=None):
    logger = get_task_logger(log_name)
    logger.setLevel('DEBUG')
    file_name = '{}_{}.log'.format(log_name, uuid.uuid4().hex)
    formatter = Formatter('%(asctime)s %(filename)s %(funcName)s[line:%(lineno)d] %(process)d %(levelname)s %(message)s')
    set_file_handler(logger, formatter, file_name, level)
    set_stream_handler(logger, formatter, level)
    return logger


def set_file_handler(logger, formatter, file_name, level=None):
    """
    set file handler
    :param level:
    :return:
    """
    # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if 'win32' in sys.platform:
        log_dir = os.path.join(base_dir, 'logs')
    else:
        log_dir = LOG_DIR
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    abs_file_name = os.path.join(log_dir, file_name)
    file_handler = ICSTimedRotatingFileHandler(filename=abs_file_name, when='MIDNIGHT', interval=1, backupCount=15)
    file_handler.suffix = '%Y-%m-%d.log'
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_stream_handler(logger, formatter, level=None):
    """
    set stream handler
    :param level:
    :return:
    """
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    log_name = 'test'
    logger = get_custom_task_logger(log_name, level='INFO')
    while True:
        logger.info('1111')
        time.sleep(1)