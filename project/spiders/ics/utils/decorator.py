#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'MaoJingwen'

import functools
import traceback
from ics.proxy import abandon_proxy
from celery.exceptions import SoftTimeLimitExceeded
from requests.exceptions import RequestException, ProxyError, ConnectTimeout, ReadTimeout, ConnectionError
from urllib3.exceptions import HTTPError

# RequestException
# HTTPError
# ConnectionError
# ProxyError
# SSLError
# Timeout
# ConnectTimeout
# ReadTimeout
# URLRequired
# TooManyRedirects
# MissingSchema
# InvalidSchema
# InvalidURL
# InvalidHeader
# ChunkedEncodingError
# ContentDecodingError
# StreamConsumedError
# RetryError
# UnrewindableBodyError


http_exception = (HTTPError, RequestException)


def stable(exc_turple, logger=None):
    def stable_(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            error_msg = None
            self.callback_param = None
            self.error_callback = None
            unexcept_error = False
            self.logger_meta = dict()
            self.abandon_ip = None
            try:
                ret = func(self, *args, **kwargs)
                return ret
            except http_exception as e:
                logger.error('task_id: {}, http_exception retry_cnt:{} ,max_retry_cnt:{}, type e: {}'.format(
                    self.callback_param['seed_dict']['task_id'], \
                    self.request.retries, self.max_retries, type(e)))
                error_msg = traceback.format_exc()
                if isinstance(e, (ProxyError, ConnectionError, ConnectTimeout, ReadTimeout)):
                    if self.abandon_ip:
                        abandon_proxy(self.abandon_ip, logger.name)
                        logger.error("abandon ip:" + self.abandon_ip)
                raise self.retry(exc=e, args=args, kwargs=kwargs)
            except SoftTimeLimitExceeded as e:
                logger.error('task_id: {}, SoftTimeLimitExceeded retry_cnt:{} ,max_retry_cnt:{}, type e: {}'.format(
                    self.callback_param['seed_dict']['task_id'], \
                    self.request.retries, self.max_retries, type(e)))
                error_msg = traceback.format_exc()
                raise self.retry(exc=e, args=args, kwargs=kwargs)
            except exc_turple as e:
                logger.error('task_id: {}, exc_turple retry_cnt:{} ,max_retry_cnt:{}, type: e: {}'.format(
                    self.callback_param['seed_dict']['task_id'], \
                    self.request.retries, \
                    self.max_retries,
                    type(e)))

                error_msg = traceback.format_exc()
                logger.warning(u'task_id: {},开始进入retry， e: {}, args: {}, kwargs: {}'.format( \
                    self.callback_param['seed_dict']['task_id'], str(e), args, kwargs))
                raise self.retry(exc=e, args=args, kwargs=kwargs)
            except Exception:
                error_msg = u'程序出现非预期异常，不重试，原因：{}'.format(traceback.format_exc())
                unexcept_error = True
            finally:
                if error_msg:
                    logger.error(
                        "Excption:" + error_msg + "\r\n" + "args:" + str(args).decode(
                            "unicode_escape") + "\r\n" + "kwargs:" + str(
                            kwargs).decode("unicode_escape"))
                    if self.logger_meta:
                        logger.error("logger_meta:" + str(self.logger_meta).decode("unicode_escape"))

                    if self.error_callback and self.callback_param:
                        if unexcept_error:
                            excption_msg = u'重试达到最大次数{}, 原因：{}'.format(self.request.retries, error_msg)
                            logger.error(excption_msg)
                            self.error_callback(self.callback_param, excption_msg)
                        elif self.request.retries == self.max_retries:
                            excption_msg = u'重试达到最大次数{}, 原因：{}'.format(self.request.retries, error_msg)
                            logger.error(excption_msg)
                            self.error_callback(self.callback_param, excption_msg)
                        else:
                            logger.info('task_id: {}, current_retry_cnt: {}, total_retry_cnt: {}'.format(
                                self.callback_param['seed_dict']['task_id'], self.request.retries, self.max_retries))

        return wrapper

    return stable_


def stable2(exc_turple, logger=None):
    def stable_(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            error_msg = None
            try:
                ret = func(self, *args, **kwargs)
                return ret

            except SoftTimeLimitExceeded as e:
                logger.error('SoftTimeLimitExceeded retry_cnt:{} ,max_retry_cnt:{}, type e: {}'.format(
                    self.request.retries, self.max_retries, type(e)))
                error_msg = traceback.format_exc()
                raise self.retry(exc=e, args=args, kwargs=kwargs)
            except exc_turple as e:
                logger.error('exc_turple retry_cnt:{} ,max_retry_cnt:{}, type: e: {}'.\
                             format(self.request.retries,self.max_retries,type(e)))

                error_msg = traceback.format_exc()
                logger.warning(u'开始进入retry， e: {}, args: {}, kwargs: {}'.format(str(e), args, kwargs))
                raise self.retry(exc=e, args=args, kwargs=kwargs)
            except Exception:
                error_msg = u'程序出现非预期异常，不重试，原因：{}'.format(traceback.format_exc())
            finally:
                if error_msg:
                    logger.error("Excption:" + error_msg + "\r\n" + \
                                 "args:" + str(args).decode("unicode_escape") + \
                                 "\r\n" + "kwargs:" + str(kwargs).decode("unicode_escape"))

                    logger.info('current_retry_cnt: {}, total_retry_cnt: {}'.\
                                        format(self.request.retries, self.max_retries))

        return wrapper

    return stable_