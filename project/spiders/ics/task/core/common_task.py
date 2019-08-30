#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.http import Response
from ics.scheduler import DownloadTask, app
from ics.proxy import get_proxy
from ics.utils.reqser import request_from_dict, request_to_dict, response_to_dict
from celery.utils.log import get_task_logger
import requests

logger = get_task_logger(__name__)


@app.task(bind=True, base=DownloadTask, default_retry_delay=10, max_retries=3, rate_limit='120/m',ignore_result=True)
def download_request(self, request_temp, queue, callback_queue):
    try:
        request = request_from_dict(request_temp)
        m_response = None

        session = requests.session()
        session.mount('https://', self._request_retry)
        session.mount('http://', self._request_retry)

        if not request.headers:
            request.headers = self._headers
            session.headers = self._headers

        if request.method.upper() == "GET":
            if self.use_proxy:
                m_proxies = get_proxy()
                m_response = session.get(
                    url=request.url,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout,
                    proxies=m_proxies
                )
            else:
                m_response = session.get(
                    url=request.url,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout
                )
        elif request.method.upper() == "POST":
            if self.use_proxy:
                m_proxies = get_proxy()
                m_response = session.post(
                    url=request.url,
                    data=request.data,
                    json=request.json,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout,
                    proxies=m_proxies
                )
            else:
                m_response = session.post(
                    url=request.url,
                    data=request.data,
                    json=request.json,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout
                )
        else:
            pass

        true_response = Response(
            m_response=m_response,
            request=request,
        )

        response_dict = response_to_dict(true_response)
        app.send_task(request.callback, [response_dict], queue=callback_queue)
        return response_dict
    except Exception as e:
        self.retry(exc=e, request_temp=request_temp, queue=queue, callback_queue=callback_queue)


# 发送下载请求 到下载队列，callback_queue 是指 下载完成后 request的回调任务 发送到哪个队列执行，默认就是下载队列，若需要设置优先级队列则需要指定回调任务在哪个队列执行
def send_download_request(request, queue, callback_queue=None):
    if callback_queue:
        app.send_task('ics.task.core.common_task.download_request',
                      [request_to_dict(request), queue, callback_queue], queue=queue)
    else:
        app.send_task('ics.task.core.common_task.download_request',
                      [request_to_dict(request), queue, queue], queue=queue)
