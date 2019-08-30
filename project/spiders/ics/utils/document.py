#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from readability.readability import Document
from bs4 import BeautifulSoup as bs


def get_summery(content):
    readable_article = Document(content).summary()
    return bs(readable_article, 'lxml').text.strip()

def get_title(content):
    readable_article = Document(content).title()
    return readable_article.strip()
