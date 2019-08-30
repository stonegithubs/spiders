#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "chiachi"


def replace_words(s, words):
    """
    对字符串中多个关键字进行同步替换的方法，优先从最长关键字开始匹配。
    :param s: 原字符串
    :param words: 待替换的关键词字典或列表。# {'待替换关键词1':'替换为此处1', ...} [('待替换关键词1', '替换为此处1'), ...]
    :return: 替换后的字符串
    """
    # escape `{` and `}`
    s = s.replace('{', '{{').replace('}', '}}')
    if isinstance(words, dict):
        words = words.items()
    words = sorted(words, key=lambda t: len(t[0]), reverse=True)
    vlist = [w[1] for w in words]
    for idx, (k, _) in enumerate(words):
        s = s.replace(k, '{%d}' % idx)
    return s.format(*vlist)


def remove_words(s, words):
    if not all(isinstance(w, basestring) for w in words):
        raise TypeError('words中所有项都应为字符串')
    return replace_words(s, [(w, '') for w in words])


if __name__ == '__main__':
    s = '原告张三诉被告李四'
    words = ['原告', '被告']
    res=  replace_words(s, {'原告': '', '被告': '', '诉': ','}) == '张三,李四'
    print (res)
    assert remove_words(s, words) == '张三诉李四'
    print remove_words('原审原告人张三诉被告李四', ['被告', '原告人', '原审原告']) #== '人张三诉李四'
