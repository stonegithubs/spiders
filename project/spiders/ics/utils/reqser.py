#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import six
import base64
from requests import Response as resp
from ics.http.spider_response import Response
from ics.http.spider_request import Request
from ics.utils.python import to_unicode, to_native_str
import requests
import chardet

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def request_to_dict(request):
    """Convert Request object to a dict.

    If a spider is given, it will try to find out the name of the spider method
    used in the callback and store that as the callback.
    """

    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': request.callback,
        'errback': request.errback,
        'data': request.data,
        'json': request.json,
        'allow_redirects': request.allow_redirects,
        'duplicate_remove': request.duplicate_remove,
        'timeout': request.timeout,
        'method': request.method,
        'headers': request.headers,
        'cookies': request.cookies,
        'meta': request.meta,
        'priority': request.priority,
        'is_img': request.is_img
    }
    return d


def request_from_dict(d):
    """Create Request object from a dict.

    If a spider is given, it will try to resolve the callbacks looking at the
    spider for methods with the same name.
    """
    return Request(
        url=to_native_str(d['url']),
        data=d['data'],
        json=d['json'],
        allow_redirects=d['allow_redirects'],
        duplicate_remove=d['duplicate_remove'],
        timeout=d['timeout'],
        callback=d['callback'],
        errback=d['errback'],
        method=d['method'],
        headers=d['headers'],
        cookies=d['cookies'],
        meta=d['meta'],
        priority=d['priority'],
        is_img=d['is_img']
    )


def _find_method(obj, func):
    if obj:
        try:
            func_self = six.get_method_self(func)
        except AttributeError:  # func has no __self__
            pass
        else:
            if func_self is obj:
                return six.get_method_function(func).__name__
    raise ValueError("Function %s is not a method of: %s" % (func, obj))


def _get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        raise ValueError("Method %r not found in: %s" % (name, obj))


def response_to_dict(response):
    if response.request.is_img:
        response.m_response._content = base64.b64encode(response.m_response._content)
    else:
        # 若content是一些不能被序列化的编码，则会造成异常，所以在这里处理
        response.m_response._content = response.m_response._content.decode(
            chardet.detect(response.m_response._content)['encoding'], 'ignore')
    d = {
        '_content': response.m_response._content,
        # '_content_consumed': response.m_response._content_consumed,
        # '_next': response.m_response._next,
        'status_code': response.m_response.status_code,
        'headers': dict(response.m_response.headers),
        # 'raw': response.m_response.raw,
        'url': to_unicode(response.m_response.url),
        'encoding': response.m_response.encoding,
        # 'history': response.m_response.history,
        # 'reason': response.m_response.reason,
        'cookies': requests.utils.dict_from_cookiejar(response.m_response.cookies),
        # 'elapsed': response.m_response.elapsed
    }
    return {'request': request_to_dict(response.request), 'm_response': d}


def response_from_dict(d):
    response = resp()
    response._content = d['m_response']['_content']
    # response._content_consumed = d['m_response']['_content_consumed']
    # response._next = d['m_response']['_next']
    response.status_code = d['m_response']['status_code']
    response.headers = d['m_response']['headers']
    # response.raw = d['m_response']['raw']
    response.url = to_native_str(d['m_response']['url'])
    response.encoding = d['m_response']['encoding']
    # response.history = d['m_response']['history']
    # response.reason = d['m_response']['reason']
    response.cookies = requests.utils.cookiejar_from_dict(d['m_response']['cookies'])
    # response.elapsed = d['m_response']['elapsed']

    request = request_from_dict(d['request'])

    my_response = Response()
    my_response.m_response = response
    my_response.request = request

    return my_response
