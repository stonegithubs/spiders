#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from celery import Task
from requests.adapters import HTTPAdapter


class DownloadTask(Task):
    def __init__(self):
        self.use_proxy = True
        self._cookies = None

        self._headers = dict()
        self._headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self._headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self._headers["Accept-Encoding"] = "gzip, deflate, sdch"
        self._headers["Accept-Language"] = "zh-CN,zh;q=0.8"
        self._request_retry = HTTPAdapter(max_retries=3)

        cookie_dict = dict()
        self._cookies = cookie_dict

    def on_success(self, retval, task_id, args, kwargs):
        # do something
        return super(DownloadTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # do something
        return super(DownloadTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # do something
        return super(DownloadTask, self).on_retry(exc, task_id, args, kwargs, einfo)


class StableTask(Task):
    def __init__(self):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        # do something
        return super(StableTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # do something
        return super(StableTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # do something
        return super(StableTask, self).on_retry(exc, task_id, args, kwargs, einfo)


