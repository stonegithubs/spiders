#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from requests.exceptions import RequestException
from urllib3.exceptions import HTTPError

requests_exception = (HTTPError, RequestException)
