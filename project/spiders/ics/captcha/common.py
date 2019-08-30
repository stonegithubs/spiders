#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'


class BaseCrackPic(object):
    def crack_captcha(self, im, codetype):
        raise NotImplementedError('func report_error must be implement')

    def report_error(self, im_id):
        raise NotImplementedError('func report_error must be implement')
