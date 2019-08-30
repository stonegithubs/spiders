#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json

__author__ = 'MaoJingwen'


def abstract(text, start, end):
    if text is None or text == '':
        return ''
    res = ''
    if start is not None and start != '':
        if start not in text:
            return res
        else:
            text = text[text.index(start) + len(start):]
    if end is not None and end != '':
        if end not in text:
            return res
        else:
            res = text[0:text.index(end)]
    else:
        res = text
    return res


def string_2_datetime(date_str):
    """
    turn string xxxx年xx月xx日 into datetime
    :return:
    """
    num_lst = re.compile('\d+').findall(date_str)
    return '-'.join(num_lst)


def is_json(raw_msg, logger=None):
    """
    用于判断一个字符串是否符合Json格式
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            dic = json.loads(raw_msg, encoding='utf-8')
            if dic:
                logger.info('{} is json str'.format(raw_msg))
            else:
                logger.warn('{} is empty json str'.format(raw_msg))
                return False
        except ValueError:
            if logger:
                logger.error('{} is not json str!'.format(raw_msg))
            return False
        return True
    else:
        return False


def is_json2(raw_msg, logger=None):
    """
    用于判断一个字符串loads两次后是否是一个字典
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(json.loads(raw_msg, encoding='utf-8'))
        except ValueError:
            if logger:
                logger.error('{} is not double json str!'.format(raw_msg))
            return False
        return True
    else:
        return False


def is_in_list(lst, string):
    """
    用于判断lst中的字符串 是否 在 string中
    :param lst:
    :param string:
    :return:
    """
    flag = False
    for item in lst:
        if item in string:
            flag = True
            break
    return flag


def remove_spaces(input_str):
    """
    remove spaces for input string
    :param input_str:
    :return:
    """
    return ''.join(re.compile('\S').findall(input_str))
