#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from posixpath import normpath
from bs4 import BeautifulSoup as bs
import json

from urlparse import urljoin, urlparse, urlunparse


class Response(object):
    def __init__(self, m_response=None, request=None):
        self.request = request
        self.m_response = m_response

    def __str__(self):
        if self.m_response:
            return "<Response [%s] [%s] [%.2f KB]>" % (
                self.m_response.status_code, self.m_response.url, (float(len(self.m_response.content)) / 1000))
        else:
            return "<Response failed: %s>" % self.request.url

    def get_soup(self):
        return bs(self.m_response.content, 'lxml')

    def get_json(self):
        return json.loads(self.m_response.content)

    def nice_join(self, url):
        url1 = urljoin(self.request.url, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def is_url(self, url):
        if re.match(r'^https?:/{2}\w.+$', url):
            return True
        else:
            return False

    __repr__ = __str__
