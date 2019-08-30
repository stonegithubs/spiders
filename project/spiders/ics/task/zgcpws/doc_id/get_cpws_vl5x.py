#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:cpws_vl5x.py
description:
author:crazy_jacky
version: 1.0
date:2018/8/3
"""
import hashlib

from base64 import b64encode as bsencode



def str2long(strings):
    """
    turn strings into long_str
    :param strings:
    :return:
    """
    long_str = 0
    for index in range(len(strings)):
        long_str += ord(strings[index]) << (index % 16)
    return str(long_str)


def str2long_en(strings):
    long_str = 0
    for index in range(len(strings)):
        long_str += (ord(strings[index]) << (index % 16)) + index
    return str(long_str)


def sub_str(strings, start=0, step=0):
    res_str = strings[start: start + step] if step else strings[start:]
    return res_str


def str2long_en2(strings, step):
    long_str = 0
    for index in range(len(strings)):
        long_str += (ord(strings[index]) << (index % 16)) + (index * step)
    return str(long_str)


def str2long_en3(strings, step):
    long_str = 0
    for index in range(len(strings)):
        long_str += (ord(strings[index]) << (index % 16)) + (index + step - ord(strings[index]))
    return str(long_str)


def hex_md5(strings):
    """
    get strings' md5 code
    :param strings:
    :return:
    """
    md5_value = hashlib.md5(strings)
    return md5_value.hexdigest()


def hex_sha1(strings):
    """
    get strings sha1 code
    :param strings:
    :return:
    """
    return hashlib.sha1(strings).hexdigest()


def char_at(strings, index):
    if index < len(strings):
        return strings[index]
    else:
        return ''


def char_code_at(strings, index):
    return ord(char_at(strings, index))


def make_key_0(strings):
    strings = sub_str(strings, 5, 5 * 5) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    result = sub_str(hex_md5(strings), 4, 24)
    return result


def make_key_1(strings):
    strings = sub_str(strings, 5, 5 * 5) + '5' + sub_str(strings, 1, 2) + '1' + sub_str(strings, (5 + 1) * (5 + 1), 3)
    a = sub_str(strings, 5) + sub_str(strings, 4)
    c = sub_str(strings, 4) + sub_str(a, 6)
    return sub_str(hex_md5(c), 4, 24)


def make_key_2(strings):
    strings = sub_str(strings, 5, 5 * 5) + '15' + sub_str(strings, 1, 2) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    b = str2long(sub_str(strings, 5)) + sub_str(strings, 4)
    c = sub_str(strings, 4) + sub_str(b, 5)
    return sub_str(hex_md5(c), 1, 24)


def make_key_3(strings):
    strings = sub_str(strings, 5, 5 * 5) + '15' + sub_str(strings, 1, 2) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    a = str2long_en(sub_str(strings, 5)) + sub_str(strings, 4)
    b = sub_str(strings, 4) + sub_str(a, 5)
    return sub_str(hex_md5(b), 3, 24)


def make_key_4(strings):
    strings = sub_str(strings, 5, 5 * 5) + '2' + sub_str(strings, 1, 2) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16)) + index
    a = str(lon) + '' + sub_str(strings, 4)
    b = hex_md5(sub_str(strings, 1)) + str2long(sub_str(a, 5))
    return sub_str(hex_md5(b), 3, 24)


def make_key_5(strings):
    strings = bsencode(sub_str(strings, 5, 5 * 5) + sub_str(strings, 1, 2) + '1').strip() + \
              sub_str(strings, (5 + 1) * (5 + 1), 3)
    return sub_str(hex_md5(strings), 4, 24)


def make_key_6(strings):
    strings = sub_str(strings, 5, 5 * 5) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    a = bsencode(sub_str(strings, 4, 10)).strip() + sub_str(strings, 2)
    b = sub_str(strings, 6) + sub_str(a, 2)
    return sub_str(hex_md5(b), 2, 24)


def make_key_7(strings):
    strings = bsencode(sub_str(strings, 5, 5 * 4) + '55' + sub_str(strings, 1, 2)).strip() + \
              sub_str(strings, (5 + 1) * (5 + 1), 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16))
    a = str(lon) + '' + sub_str(strings, 4)
    b = hex_md5(sub_str(strings, 1)) + str2long(sub_str(a, 5))
    return sub_str(hex_md5(b), 3, 24)


def make_key_8(strings):
    strings = bsencode(sub_str(strings, 5, 5 * 5 - 1) + '5' + '-' + '5').strip() + sub_str(strings, 1, 2) + \
              sub_str(strings, (5 + 1) * (5 + 1), 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16))
    a = str(lon) + '' + sub_str(strings, 4)
    b = hex_md5(sub_str(strings, 1)) + str2long_en(sub_str(a, 5))
    return sub_str(hex_md5(b), 4, 24)


def make_key_9(strings):
    strings = sub_str(strings, 5, 5 * 5) + '5' + sub_str(strings, 1, 2) + '1' + sub_str(strings, (5 + 1) * (5 + 1), 3)
    a = sub_str(strings, 5) + sub_str(strings, 4)
    c = hex_sha1(sub_str(strings, 4)) + sub_str(a, 6)
    return sub_str(hex_md5(c), 4, 24)


def make_key_10(strings):
    strings = bsencode(sub_str(strings, 5, 5 * 5 - 1) + '5').strip() + sub_str(strings, 1, 2) + \
              sub_str(strings, (5 + 1) * (5 + 1), 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16))
    a = str(lon) + '' + sub_str(strings, 4)
    b = hex_md5(sub_str(strings, 1)) + hex_sha1(sub_str(a, 5))
    return sub_str(hex_md5(b), 4, 24)


def make_key_11(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '2' + sub_str(strings, 1, 2) + sub_str(strings, (5 + 1) * (5 + 1), 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16))
    a = str(lon) + '' + sub_str(strings, 2)
    b = sub_str(strings, 1) + hex_sha1(sub_str(a, 5))
    return sub_str(hex_md5(b), 2, 24)


def make_key_12(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + sub_str(strings, (5 + 1) * (5 + 1), 3) + '2' + sub_str(strings, 1, 2)
    b = sub_str(strings, 1) + hex_sha1(sub_str(strings, 5))
    return sub_str(hex_md5(b), 1, 24)


def make_key_13(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '2' + sub_str(strings, 1, 2)
    b = bsencode(sub_str(strings, 1) + hex_sha1(sub_str(strings, 5))).strip()
    return sub_str(hex_md5(b), 1, 24)


def make_key_14(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '2' + sub_str(strings, 1, 2)
    b = bsencode(sub_str(strings, 1) + sub_str(strings, 5) + sub_str(strings, 1, 3)).strip()
    return sub_str(hex_sha1(b), 1, 24)


def make_key_15(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '2' + sub_str(strings, 1, 2)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16))
    a = str(lon) + '' + sub_str(strings, 2)
    b = bsencode(sub_str(a, 1) + sub_str(strings, 5) + sub_str(strings, 2, 3)).strip()
    return sub_str(hex_sha1(b), 1, 24)


def make_key_16(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '2' + sub_str(strings, 1, 2) + '-' + '5'
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16)) + index
    a = str(lon) + '' + sub_str(strings, 2)
    b = bsencode(sub_str(a, 1)).strip() + str2long_en2(sub_str(strings, 5), 5) + sub_str(strings, 2, 3)
    return sub_str(hex_md5(b), 2, 24)


def make_key_17(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '7' + sub_str(strings, 1, 2) + '-' + '5'
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16)) + index
    a = str(lon) + '' + sub_str(strings, 2)
    b = bsencode(sub_str(a, 1)).strip() + str2long_en2(sub_str(strings, 5), 5 + 1) + sub_str(strings, 2 + 5, 3)
    return sub_str(hex_md5(b), 0, 24)


def make_key_18(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '7' + sub_str(strings, 1, 2) + '5' + sub_str(strings, 2 + 5, 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16)) + index
    a = str(lon) + '' + sub_str(strings, 2)
    b = sub_str(a, 1) + str2long_en2(sub_str(strings, 5), 5 + 1) + sub_str(strings, 2 + 5, 3)
    return sub_str(hex_md5(b), 0, 24)


def make_key_19(strings):
    strings = sub_str(strings, 5, 5 * 5 - 1) + '7' + sub_str(strings, 5, 2) + '5' + sub_str(strings, 2 + 5, 3)
    lon = 0
    a = sub_str(strings, 5)
    for index in range(len(a)):
        lon += (char_code_at(a, index) << (index % 16)) + index
    a = str(lon) + '' + sub_str(strings, 2)
    b = sub_str(a, 1) + str2long_en3(sub_str(strings, 5), 5 - 1) + sub_str(strings, 2 + 5, 3)
    return sub_str(hex_md5(b), 0, 24)


def make_key_20(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings)), 1, 24)


def make_key_21(strings):
    return sub_str(hex_md5(make_key_11(strings) + make_key_3(strings)), 2, 24)


def make_key_22(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings)), 3, 24)


def make_key_23(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings)), 4, 24)


def make_key_24(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings)), 1, 24)


def make_key_25(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 2, 24)


def make_key_26(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings)), 3, 24)


def make_key_27(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings)), 4, 24)


def make_key_28(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings)), 1, 24)


def make_key_29(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings)), 2, 24)


def make_key_30(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings)), 3, 24)


def make_key_31(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings)), 4, 24)


def make_key_32(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings)), 3, 24)


def make_key_33(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings)), 4, 24)


def make_key_34(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings)), 1, 24)


def make_key_35(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_9(strings)), 2, 24)


def make_key_36(strings):
    return sub_str(hex_md5(make_key_8(strings) + make_key_10(strings)), 3, 24)


def make_key_37(strings):
    return sub_str(hex_md5(make_key_6(strings) + make_key_17(strings)), 1, 24)


def make_key_38(strings):
    return sub_str(hex_md5(make_key_12(strings) + make_key_18(strings)), 2, 24)


def make_key_39(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings)), 3, 24)


def make_key_40(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings)), 4, 24)


def make_key_41(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings)), 3, 24)


def make_key_42(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 4, 24)


def make_key_43(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings)), 1, 24)


def make_key_44(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings)), 2, 24)


def make_key_45(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings)), 3, 24)


def make_key_46(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_17(strings)), 4, 24)


def make_key_47(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_18(strings)), 1, 24)


def make_key_48(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings)), 2, 24)


def make_key_49(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings)), 3, 24)


def make_key_50(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_1(strings)), 4, 24)


def make_key_51(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings)), 1, 24)


def make_key_52(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_14(strings)), 2, 24)


def make_key_53(strings):
    return sub_str(hex_md5(make_key_12(strings) + make_key_15(strings)), 3, 24)


def make_key_54(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_16(strings)), 4, 24)


def make_key_55(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_9(strings)), 3, 24)


def make_key_56(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_10(strings)), 4, 24)


def make_key_57(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_17(strings)), 1, 24)


def make_key_58(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_18(strings)), 2, 24)


def make_key_59(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_19(strings)), 3, 24)


def make_key_60(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings)), 1, 24)


def make_key_61(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings)), 2, 24)


def make_key_62(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings)), 3, 24)


def make_key_63(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings)), 4, 24)


def make_key_64(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings)), 3, 24)


def make_key_65(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_1(strings)), 1, 24)


def make_key_66(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_4(strings)), 2, 24)


def make_key_67(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_5(strings)), 3, 24)


def make_key_68(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_3(strings)), 4, 24)


def make_key_69(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_7(strings)), 1, 24)


def make_key_70(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_0(strings)), 2, 24)


def make_key_71(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_1(strings)), 3, 24)


def make_key_72(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_4(strings)), 4, 24)


def make_key_73(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings)), 1, 24)


def make_key_74(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings)), 2, 24)


def make_key_75(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings)), 3, 24)


def make_key_76(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings)), 4, 24)


def make_key_77(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings)), 3, 24)


def make_key_78(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 4, 24)


def make_key_79(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_9(strings)), 1, 24)


def make_key_80(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_10(strings)), 2, 24)


def make_key_81(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 3, 24)


def make_key_82(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_18(strings)), 1, 24)


def make_key_83(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_19(strings)), 4, 24)


def make_key_84(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_0(strings)), 1, 24)


def make_key_85(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_1(strings)), 2, 24)


def make_key_86(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_4(strings)), 3, 24)


def make_key_87(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_14(strings)), 4, 24)


def make_key_88(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_15(strings)), 1, 24)


def make_key_89(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_16(strings)), 2, 24)


def make_key_90(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_9(strings)), 3, 24)


def make_key_91(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_10(strings)), 4, 24)


def make_key_92(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings)), 3, 24)


def make_key_93(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings)), 4, 24)


def make_key_94(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 1, 24)


def make_key_95(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 2, 24)


def make_key_96(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 3, 24)


def make_key_97(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 4, 24)


def make_key_98(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_5(strings)), 3, 24)


def make_key_99(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_3(strings)), 4, 24)


def make_key_100(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_3(strings)), 1, 24)


def make_key_101(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_7(strings)), 2, 24)


def make_key_102(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_18(strings)), 1, 24)


def make_key_103(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 2, 24)


def make_key_104(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 3, 24)


def make_key_105(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 4, 24)


def make_key_106(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 1, 24)


def make_key_107(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_14(strings)), 2, 24)


def make_key_108(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_15(strings)), 3, 24)


def make_key_109(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_16(strings)), 4, 24)


def make_key_110(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_9(strings)), 1, 24)


def make_key_111(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_10(strings)), 2, 24)


def make_key_112(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings)), 3, 24)


def make_key_113(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings)), 4, 24)


def make_key_114(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 3, 24)


def make_key_115(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 4, 24)


def make_key_116(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 1, 24)


def make_key_117(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 2, 24)


def make_key_118(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings)), 3, 24)


def make_key_119(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings)), 1, 24)


def make_key_120(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_9(strings)), 1, 24)


def make_key_121(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_10(strings)), 2, 24)


def make_key_122(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_17(strings)), 3, 24)


def make_key_123(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_18(strings)), 4, 24)


def make_key_124(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_19(strings)), 1, 24)


def make_key_125(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_0(strings)), 2, 24)


def make_key_126(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings)), 3, 24)


def make_key_127(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings)), 4, 24)


def make_key_128(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_5(strings)), 1, 24)


def make_key_129(strings):
    return sub_str(hex_md5(make_key_8(strings) + make_key_3(strings)), 2, 24)


def make_key_130(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_7(strings)), 3, 24)


def make_key_131(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_10(strings)), 4, 24)


def make_key_132(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_17(strings)), 3, 24)


def make_key_133(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_18(strings)), 4, 24)


def make_key_134(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_19(strings)), 1, 24)


def make_key_135(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_0(strings)), 2, 24)


def make_key_136(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_1(strings)), 1, 24)


def make_key_137(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_14(strings)), 2, 24)


def make_key_138(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_15(strings)), 3, 24)


def make_key_139(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_16(strings)), 4, 24)


def make_key_140(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_9(strings)), 1, 24)


def make_key_141(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_10(strings)), 2, 24)


def make_key_142(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_17(strings)), 3, 24)


def make_key_143(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_18(strings)), 4, 24)


def make_key_144(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_19(strings)), 1, 24)


def make_key_145(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings)), 2, 24)


def make_key_146(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings)), 3, 24)


def make_key_147(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings)), 4, 24)


def make_key_148(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings)), 3, 24)


def make_key_149(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings)), 4, 24)


def make_key_150(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings)), 1, 24)


def make_key_151(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings)), 2, 24)


def make_key_152(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings)), 3, 24)


def make_key_153(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 1, 24)


def make_key_154(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings)), 1, 24)


def make_key_155(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings)), 2, 24)


def make_key_156(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings)), 3, 24)


def make_key_157(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings)), 4, 24)


def make_key_158(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings)), 1, 24)


def make_key_159(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings)), 2, 24)


def make_key_160(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings)), 3, 24)


def make_key_161(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings)), 4, 24)


def make_key_162(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings)), 1, 24)


def make_key_163(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings)), 2, 24)


def make_key_164(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings)), 3, 24)


def make_key_165(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_17(strings)), 4, 24)


def make_key_166(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_18(strings)), 3, 24)


def make_key_167(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_19(strings)), 4, 24)


def make_key_168(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 1, 24)


def make_key_169(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 2, 24)


def make_key_170(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 3, 24)


def make_key_171(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_5(strings)), 1, 24)


def make_key_172(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_3(strings)), 2, 24)


def make_key_173(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_7(strings)), 3, 24)


def make_key_174(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings)), 4, 24)


def make_key_175(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings)), 1, 24)


def make_key_176(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings)), 2, 24)


def make_key_177(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings)), 3, 24)


def make_key_178(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings)), 4, 24)


def make_key_179(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings)), 1, 24)


def make_key_180(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_14(strings)), 3, 24)


def make_key_181(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings)), 1, 24)


def make_key_182(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings)), 2, 24)


def make_key_183(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings)), 3, 24)


def make_key_184(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings)), 4, 24)


def make_key_185(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_17(strings)), 3, 24)


def make_key_186(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_18(strings)), 4, 24)


def make_key_187(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_19(strings)), 4, 24)


def make_key_188(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings)), 1, 24)


def make_key_189(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings)), 2, 24)


def make_key_190(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings)), 3, 24)


def make_key_191(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 4, 24)


def make_key_192(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 1, 24)


def make_key_193(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings)), 2, 24)


def make_key_194(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings)), 3, 24)


def make_key_195(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings)), 4, 24)


def make_key_196(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings)), 3, 24)


def make_key_197(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings)), 4, 24)


def make_key_198(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_9(strings)), 1, 24)


def make_key_199(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings)), 2, 24)


def make_key_200(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 2, 24)


def make_key_201(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 3, 24)


def make_key_202(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings)), 1, 24)


def make_key_203(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings)), 2, 24)


def make_key_204(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_5(strings)), 3, 24)


def make_key_205(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_3(strings)), 4, 24)


def make_key_206(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_7(strings)), 1, 24)


def make_key_207(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_17(strings)), 2, 24)


def make_key_208(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_18(strings)), 3, 24)


def make_key_209(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_19(strings)), 4, 24)


def make_key_210(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_0(strings)), 1, 24)


def make_key_211(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_1(strings)), 3, 24)


def make_key_212(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_4(strings)), 1, 24)


def make_key_213(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_14(strings)), 2, 24)


def make_key_214(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_15(strings)), 3, 24)


def make_key_215(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_16(strings)), 4, 24)


def make_key_216(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_9(strings)), 3, 24)


def make_key_217(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_10(strings)), 4, 24)


def make_key_218(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_17(strings)), 4, 24)


def make_key_219(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_18(strings)), 1, 24)


def make_key_220(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_19(strings)), 2, 24)


def make_key_221(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_0(strings)), 3, 24)


def make_key_222(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings)), 4, 24)


def make_key_223(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings)), 1, 24)


def make_key_224(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings)), 2, 24)


def make_key_225(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings)), 3, 24)


def make_key_226(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_7(strings)), 4, 24)


def make_key_227(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 2, 24)


def make_key_228(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 3, 24)


def make_key_229(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 1, 24)


def make_key_230(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 2, 24)


def make_key_231(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 3, 24)


def make_key_232(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 4, 24)


def make_key_233(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_14(strings)), 1, 24)


def make_key_234(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_15(strings)), 2, 24)


def make_key_235(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_16(strings)), 3, 24)


def make_key_236(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_9(strings)), 4, 24)


def make_key_237(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_10(strings)), 1, 24)


def make_key_238(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_17(strings)), 3, 24)


def make_key_239(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings)), 1, 24)


def make_key_240(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_0(strings)), 2, 24)


def make_key_241(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_1(strings)), 3, 24)


def make_key_242(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_4(strings)), 4, 24)


def make_key_243(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_5(strings)), 3, 24)


def make_key_244(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_3(strings)), 4, 24)


def make_key_245(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_7(strings)), 4, 24)


def make_key_246(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 2, 24)


def make_key_247(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 3, 24)


def make_key_248(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 1, 24)


def make_key_249(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 2, 24)


def make_key_250(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 3, 24)


def make_key_251(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_4(strings)), 4, 24)


def make_key_252(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_14(strings)), 1, 24)


def make_key_253(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_15(strings)), 2, 24)


def make_key_254(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 3, 24)


def make_key_255(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_14(strings)), 4, 24)


def make_key_256(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_15(strings)), 1, 24)


def make_key_257(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_16(strings)), 3, 24)


def make_key_258(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_9(strings)), 1, 24)


def make_key_259(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_10(strings)), 2, 24)


def make_key_260(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_17(strings)), 3, 24)


def make_key_261(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_18(strings)), 4, 24)


def make_key_262(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 3, 24)


def make_key_263(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 4, 24)


def make_key_264(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings)), 4, 24)


def make_key_265(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings)), 1, 24)


def make_key_266(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings)), 2, 24)


def make_key_267(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings)), 3, 24)


def make_key_268(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings)), 4, 24)


def make_key_269(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings)), 1, 24)


def make_key_270(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_14(strings)), 2, 24)


def make_key_271(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings)), 3, 24)


def make_key_272(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings)), 4, 24)


def make_key_273(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings)), 3, 24)


def make_key_274(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings)), 4, 24)


def make_key_275(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 1, 24)


def make_key_276(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 2, 24)


def make_key_277(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 2, 24)


def make_key_278(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_4(strings)), 3, 24)


def make_key_279(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_5(strings)), 1, 24)


def make_key_280(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_3(strings)), 2, 24)


def make_key_281(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_7(strings)), 3, 24)


def make_key_282(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 4, 24)


def make_key_283(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 1, 24)


def make_key_284(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 2, 24)


def make_key_285(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 3, 24)


def make_key_286(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 4, 24)


def make_key_287(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_4(strings)), 1, 24)


def make_key_288(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_14(strings)), 3, 24)


def make_key_289(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_15(strings)), 1, 24)


def make_key_290(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_16(strings)), 2, 24)


def make_key_291(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_9(strings)), 3, 24)


def make_key_292(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_10(strings)), 4, 24)


def make_key_293(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 3, 24)


def make_key_294(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings)), 4, 24)


def make_key_295(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 4, 24)


def make_key_296(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 1, 24)


def make_key_297(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 2, 24)


def make_key_298(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 3, 24)


def make_key_299(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_5(strings)), 4, 24)


def make_key_300(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_3(strings)), 1, 24)


def make_key_301(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_7(strings)), 2, 24)


def make_key_302(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings)), 3, 24)


def make_key_303(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings)), 4, 24)


def make_key_304(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 3, 24)


def make_key_305(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 4, 24)


def make_key_306(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 1, 24)


def make_key_307(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 2, 24)


def make_key_308(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_14(strings)), 2, 24)


def make_key_309(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_15(strings)), 3, 24)


def make_key_310(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_16(strings)), 1, 24)


def make_key_311(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_9(strings)), 2, 24)


def make_key_312(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_10(strings)), 3, 24)


def make_key_313(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings)), 4, 24)


def make_key_314(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 1, 24)


def make_key_315(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 2, 24)


def make_key_316(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 3, 24)


def make_key_317(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 4, 24)


def make_key_318(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_5(strings)), 1, 24)


def make_key_319(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_3(strings)), 3, 24)


def make_key_320(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_7(strings)), 1, 24)


def make_key_321(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings)), 2, 24)


def make_key_322(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings)), 3, 24)


def make_key_323(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings)), 4, 24)


def make_key_324(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings)), 3, 24)


def make_key_325(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings)), 4, 24)


def make_key_326(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings)), 4, 24)


def make_key_327(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_14(strings)), 1, 24)


def make_key_328(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_15(strings)), 2, 24)


def make_key_329(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_16(strings)), 3, 24)


def make_key_330(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_9(strings)), 4, 24)


def make_key_331(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_10(strings)), 1, 24)


def make_key_332(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings)), 2, 24)


def make_key_333(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings)), 3, 24)


def make_key_334(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_18(strings)), 4, 24)


def make_key_335(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_19(strings)), 3, 24)


def make_key_336(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_0(strings)), 4, 24)


def make_key_337(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings)), 2, 24)


def make_key_338(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings)), 3, 24)


def make_key_339(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings)), 1, 24)


def make_key_340(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings)), 2, 24)


def make_key_341(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_7(strings)), 3, 24)


def make_key_342(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 4, 24)


def make_key_343(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 1, 24)


def make_key_344(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 2, 24)


def make_key_345(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 3, 24)


def make_key_346(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 4, 24)


def make_key_347(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings)), 1, 24)


def make_key_348(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_14(strings)), 3, 24)


def make_key_349(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_15(strings)), 1, 24)


def make_key_350(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_16(strings)), 2, 24)


def make_key_351(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_9(strings)), 3, 24)


def make_key_352(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_10(strings)), 4, 24)


def make_key_353(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_17(strings)), 3, 24)


def make_key_354(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 4, 24)


def make_key_355(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 4, 24)


def make_key_356(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings)), 1, 24)


def make_key_357(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings)), 2, 24)


def make_key_358(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_5(strings)), 3, 24)


def make_key_359(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_3(strings)), 4, 24)


def make_key_360(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_7(strings)), 2, 24)


def make_key_361(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_17(strings)), 3, 24)


def make_key_362(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_18(strings)), 1, 24)


def make_key_363(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings)), 2, 24)


def make_key_364(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings)), 3, 24)


def make_key_365(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings)), 4, 24)


def make_key_366(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings)), 1, 24)


def make_key_367(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_7(strings)), 2, 24)


def make_key_368(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_17(strings)), 3, 24)


def make_key_369(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_18(strings)), 4, 24)


def make_key_370(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_19(strings)), 1, 24)


def make_key_371(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings)), 3, 24)


def make_key_372(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings)), 1, 24)


def make_key_373(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings)), 2, 24)


def make_key_374(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_17(strings)), 3, 24)


def make_key_375(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_18(strings)), 4, 24)


def make_key_376(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings)), 3, 24)


def make_key_377(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings)), 4, 24)


def make_key_378(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_1(strings)), 4, 24)


def make_key_379(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings)), 1, 24)


def make_key_380(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_9(strings)), 2, 24)


def make_key_381(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_10(strings)), 3, 24)


def make_key_382(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 4, 24)


def make_key_383(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 1, 24)


def make_key_384(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 2, 24)


def make_key_385(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 3, 24)


def make_key_386(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_1(strings)), 4, 24)


def make_key_387(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_1(strings)), 2, 24)


def make_key_388(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_4(strings)), 3, 24)


def make_key_389(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_7(strings)), 1, 24)


def make_key_390(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings)), 2, 24)


def make_key_391(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings)), 3, 24)


def make_key_392(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings)), 4, 24)


def make_key_393(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings)), 1, 24)


def make_key_394(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings)), 2, 24)


def make_key_395(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings)), 3, 24)


def make_key_396(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings)), 4, 24)


def make_key_397(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings)), 1, 24)


def make_key_398(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings)), 3, 24)


def make_key_399(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_0(strings)), 1, 24)


def get_vl5x(vjkl5, logger):
    """
    calculate vl5x vy vjkl5
    :param vjkl5:
    :param logger:
    :return:
    """
    func_len = 400
    num = int(str2long(vjkl5))
    index = num % func_len
    call_func = 'make_key_{}("{}")'.format(index, vjkl5)
    logger.info('begin to excute func {}'.format(call_func))
    res = eval(call_func)
    return res