#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from bs4 import BeautifulSoup as bs


def clear_noise(src, noise_class='.dp'):
    soup = bs(src, 'lxml')
    [item.extract() for item in soup.select(noise_class)]
    return soup.text
