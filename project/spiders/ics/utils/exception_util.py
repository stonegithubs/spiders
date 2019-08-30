#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wuyong'


class LogicException(Exception):
    def __init__(self, msg):
        self.message = str(msg)
        Exception.__init__(self, msg)


class DownloaderException(Exception):
    def __init__(self, msg):
        self.message = str(msg)
        Exception.__init__(self, msg)
