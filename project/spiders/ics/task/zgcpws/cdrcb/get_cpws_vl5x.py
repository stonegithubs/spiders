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
from base64 import b64encode as bsencode
import hashlib


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
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'saf'), 1, 24)


def make_key_21(strings):
    return sub_str(hex_md5(make_key_11(strings) + make_key_3(strings) + 'vr4'), 2, 24)


def make_key_22(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'e'), 3, 24)


def make_key_23(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'vr6'), 4, 24)


def make_key_24(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'vr7'), 1, 24)


def make_key_25(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'vr8'), 2, 24)


def make_key_26(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'vr9'), 3, 24)


def make_key_27(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'vr10'), 4, 24)


def make_key_28(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings) + 'vr11'), 1, 24)


def make_key_29(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings) + 'vr12'), 2, 24)


def make_key_30(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings) + 'vr13'), 3, 24)


def make_key_31(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings) + 'vr14'), 4, 24)


def make_key_32(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'vr15'), 3, 24)


def make_key_33(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings) + 'vr16'), 4, 24)


def make_key_34(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings) + 'vr17'), 1, 24)


def make_key_35(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_9(strings) + 'vr18'), 2, 24)


def make_key_36(strings):
    return sub_str(hex_md5(make_key_8(strings) + make_key_10(strings) + 'vr19'), 3, 24)


def make_key_37(strings):
    return sub_str(hex_md5(make_key_6(strings) + make_key_17(strings) + 'vr20'), 1, 24)


def make_key_38(strings):
    return sub_str(hex_md5(make_key_12(strings) + make_key_18(strings) + 'vr21'), 2, 24)


def make_key_39(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'vr22'), 3, 24)


def make_key_40(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'vr23'), 4, 24)


def make_key_41(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'vr24'), 3, 24)


def make_key_42(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'vr25'), 4, 24)


def make_key_43(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'vr26'), 1, 24)


def make_key_44(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'vr27'), 2, 24)


def make_key_45(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings) + 'vr28'), 3, 24)


def make_key_46(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_17(strings) + 'vr29'), 4, 24)


def make_key_47(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_18(strings) + 'vr30'), 1, 24)


def make_key_48(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings) + 'vr31'), 2, 24)


def make_key_49(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings) + 'vr32'), 3, 24)


def make_key_50(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_1(strings) + 'vr33'), 4, 24)


def make_key_51(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings) + 'saf'), 1, 24)


def make_key_52(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_14(strings) + 'vr4'), 2, 24)


def make_key_53(strings):
    return sub_str(hex_md5(make_key_12(strings) + make_key_15(strings) + 'e'), 3, 24)


def make_key_54(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_16(strings) + 'l65a'), 4, 24)


def make_key_55(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_9(strings) + 'l66a'), 3, 24)


def make_key_56(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_10(strings) + 'l67a'), 4, 24)


def make_key_57(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_17(strings) + 'l68a'), 1, 24)


def make_key_58(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_18(strings) + 'l69a'), 2, 24)


def make_key_59(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_19(strings) + 'l70a'), 3, 24)


def make_key_60(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings) + 'l71a'), 1, 24)


def make_key_61(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'l72a'), 2, 24)


def make_key_62(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'l73a'), 3, 24)


def make_key_63(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings) + 'vr46'), 4, 24)


def make_key_64(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings) + 'vr47'), 3, 24)


def make_key_65(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_1(strings) + 'vr48'), 1, 24)


def make_key_66(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_4(strings) + 'vr49'), 2, 24)


def make_key_67(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_5(strings) + 'vr50'), 3, 24)


def make_key_68(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_3(strings) + 'at4'), 4, 24)


def make_key_69(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_7(strings) + 'at5'), 1, 24)


def make_key_70(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_0(strings) + 'at6'), 2, 24)


def make_key_71(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_1(strings) + 'at7'), 3, 24)


def make_key_72(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_4(strings) + 'at8'), 4, 24)


def make_key_73(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings) + 'at9'), 1, 24)


def make_key_74(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings) + 'at10'), 2, 24)


def make_key_75(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'at11'), 3, 24)


def make_key_76(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'at12'), 4, 24)


def make_key_77(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'at13'), 3, 24)


def make_key_78(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'at14'), 4, 24)


def make_key_79(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_9(strings) + 'at15'), 1, 24)


def make_key_80(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_10(strings) + 'at16'), 2, 24)


def make_key_81(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_17(strings) + 'at17'), 3, 24)


def make_key_82(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_18(strings) + 'at18'), 1, 24)


def make_key_83(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_19(strings) + 'at19'), 4, 24)


def make_key_84(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_0(strings) + 'at20'), 1, 24)


def make_key_85(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_1(strings) + 'at21'), 2, 24)


def make_key_86(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_4(strings) + 'at22'), 3, 24)


def make_key_87(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_14(strings) + 'at23'), 4, 24)


def make_key_88(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_15(strings) + 'at24'), 1, 24)


def make_key_89(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_16(strings) + 'at25'), 2, 24)


def make_key_90(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_9(strings) + 'at26'), 3, 24)


def make_key_91(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_10(strings) + 'at27'), 4, 24)


def make_key_92(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings) + 'at28'), 3, 24)


def make_key_93(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings) + 'at29'), 4, 24)


def make_key_94(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings) + 'at30'), 1, 24)


def make_key_95(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings) + 'at31'), 2, 24)


def make_key_96(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings) + 'at32'), 3, 24)


def make_key_97(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings) + 'lb73a'), 4, 24)


def make_key_98(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_5(strings) + 'lb74a'), 3, 24)


def make_key_99(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_3(strings) + 'lb75a'), 4, 24)


def make_key_100(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_3(strings) + 'lb76a'), 1, 24)


def make_key_101(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_7(strings) + 'lb77a'), 2, 24)


def make_key_102(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_18(strings) + 'lb78a'), 1, 24)


def make_key_103(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings) + 'lb79a'), 2, 24)


def make_key_104(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings) + 'lb80a'), 3, 24)


def make_key_105(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings) + 'lb81a'), 4, 24)


def make_key_106(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings) + 'l82a'), 1, 24)


def make_key_107(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_14(strings) + 'at43'), 2, 24)


def make_key_108(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_15(strings) + 'at44'), 3, 24)


def make_key_109(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_16(strings) + 'at45'), 4, 24)


def make_key_110(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_9(strings) + 'at46'), 1, 24)


def make_key_111(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_10(strings) + 'at47'), 2, 24)


def make_key_112(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_17(strings) + 'at48'), 3, 24)


def make_key_113(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_18(strings) + 'at49'), 4, 24)


def make_key_114(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_19(strings) + 'ff31'), 3, 24)


def make_key_115(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings) + 'ff32'), 4, 24)


def make_key_116(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings) + 'ff33'), 1, 24)


def make_key_117(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings) + 'ff34'), 2, 24)


def make_key_118(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings) + 'ff35'), 3, 24)


def make_key_119(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings) + 'ff36'), 1, 24)


def make_key_120(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_9(strings) + 'ff37'), 1, 24)


def make_key_121(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_10(strings) + 'ssa32'), 2, 24)


def make_key_122(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_17(strings) + 'ssa33'), 3, 24)


def make_key_123(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_18(strings) + 'ssa34'), 4, 24)


def make_key_124(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_19(strings) + 'ssa35'), 1, 24)


def make_key_125(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_0(strings) + 'ssa36'), 2, 24)


def make_key_126(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings) + 'ff43'), 3, 24)


def make_key_127(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings) + 'ff44'), 4, 24)


def make_key_128(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_5(strings) + 'ff45'), 1, 24)


def make_key_129(strings):
    return sub_str(hex_md5(make_key_8(strings) + make_key_3(strings) + 'ff46'), 2, 24)


def make_key_130(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_7(strings) + 'at45'), 3, 24)


def make_key_131(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_10(strings) + 'at46'), 4, 24)


def make_key_132(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_17(strings) + 'at47'), 3, 24)


def make_key_133(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_18(strings) + 'at48'), 4, 24)


def make_key_134(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_19(strings) + 'at49'), 1, 24)


def make_key_135(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_0(strings) + 'ff31'), 2, 24)


def make_key_136(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_1(strings) + 'ff32'), 1, 24)


def make_key_137(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_14(strings) + 'ff33'), 2, 24)


def make_key_138(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_15(strings) + 'ff55'), 3, 24)


def make_key_139(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_16(strings) + 'ff56'), 4, 24)


def make_key_140(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_9(strings) + 'ff57'), 1, 24)


def make_key_141(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_10(strings) + 'ff58'), 2, 24)


def make_key_142(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_17(strings) + 'ff59'), 3, 24)


def make_key_143(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_18(strings) + 'ff60'), 4, 24)


def make_key_144(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_19(strings) + 'ff61'), 1, 24)


def make_key_145(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings) + 'ff62'), 2, 24)


def make_key_146(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'ff63'), 3, 24)


def make_key_147(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'ff64'), 4, 24)


def make_key_148(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings) + 'ff65'), 3, 24)


def make_key_149(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings) + 'ff66'), 4, 24)


def make_key_150(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'ff67'), 1, 24)


def make_key_151(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'ff68'), 2, 24)


def make_key_152(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'ff69'), 3, 24)


def make_key_153(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'ff70'), 1, 24)


def make_key_154(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'ff71'), 1, 24)


def make_key_155(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'ff72'), 2, 24)


def make_key_156(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings) + 'ff73'), 3, 24)


def make_key_157(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings) + 'ff74'), 4, 24)


def make_key_158(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings) + 'ff75'), 1, 24)


def make_key_159(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings) + 'ff76'), 2, 24)


def make_key_160(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'ff77'), 3, 24)


def make_key_161(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings) + 'ff78'), 4, 24)


def make_key_162(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings) + 'ff79'), 1, 24)


def make_key_163(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings) + 'ff80'), 2, 24)


def make_key_164(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings) + 'ff81'), 3, 24)


def make_key_165(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_17(strings) + 'ff82'), 4, 24)


def make_key_166(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_18(strings) + 'ff83'), 3, 24)


def make_key_167(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_19(strings) + 'ff84'), 4, 24)


def make_key_168(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_0(strings) + 'ff85'), 1, 24)


def make_key_169(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings) + 'ff105'), 2, 24)


def make_key_170(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings) + 'ff106'), 3, 24)


def make_key_171(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_5(strings) + 'ff107'), 1, 24)


def make_key_172(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_3(strings) + 'ff108'), 2, 24)


def make_key_173(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_7(strings) + 'ff109'), 3, 24)


def make_key_174(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_17(strings) + 'aa0'), 4, 24)


def make_key_175(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings) + 'aa1'), 1, 24)


def make_key_176(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings) + 'aa2'), 2, 24)


def make_key_177(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings) + 'aa3'), 3, 24)


def make_key_178(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings) + 'aa4'), 4, 24)


def make_key_179(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings) + 'aa5'), 1, 24)


def make_key_180(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_14(strings) + 'aa6'), 3, 24)


def make_key_181(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings) + 'ff98'), 1, 24)


def make_key_182(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings) + 'ff99'), 2, 24)


def make_key_183(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings) + 'ff100'), 3, 24)


def make_key_184(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings) + 'ff101'), 4, 24)


def make_key_185(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_17(strings) + 'ff102'), 3, 24)


def make_key_186(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_18(strings) + 'ff103'), 4, 24)


def make_key_187(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_19(strings) + 'ff104'), 4, 24)


def make_key_188(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_0(strings) + 'ff105'), 1, 24)


def make_key_189(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings) + 'ff106'), 2, 24)


def make_key_190(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings) + 'ff107'), 3, 24)


def make_key_191(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings) + 'ff108'), 4, 24)


def make_key_192(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings) + 'ff109'), 1, 24)


def make_key_193(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings) + 'aa0'), 2, 24)


def make_key_194(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings) + 'aa1'), 3, 24)


def make_key_195(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'aa2'), 4, 24)


def make_key_196(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings) + 'aa3'), 3, 24)


def make_key_197(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings) + 'aa4'), 4, 24)


def make_key_198(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_9(strings) + 'aa5'), 1, 24)


def make_key_199(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_1(strings) + 'aa6'), 2, 24)


def make_key_200(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings) + 'aa7'), 2, 24)


def make_key_201(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'aa8'), 3, 24)


def make_key_202(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'aa9'), 4, 24)


def make_key_203(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings) + 'aa10'), 4, 24)


def make_key_204(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings) + 'aa11'), 1, 24)


def make_key_205(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'aa12'), 2, 24)


def make_key_206(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'aa13'), 2, 24)


def make_key_207(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'aa14'), 3, 24)


def make_key_208(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'xx32'), 4, 24)


def make_key_209(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'xx33'), 3, 24)


def make_key_210(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'xx34'), 4, 24)


def make_key_211(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings) + 'xx35'), 1, 24)


def make_key_212(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings) + 'xx36'), 4, 24)


def make_key_213(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings) + 'xx37'), 1, 24)


def make_key_214(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings) + 'xx38'), 3, 24)


def make_key_215(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'xx39'), 4, 24)


def make_key_216(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings) + 'xx40'), 1, 24)


def make_key_217(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings) + 'xx41'), 4, 24)


def make_key_218(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings) + 'xx42'), 1, 24)


def make_key_219(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings) + 'xx43'), 2, 24)


def make_key_220(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_17(strings) + 'xx44'), 3, 24)


def make_key_221(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_1(strings) + 'xx45'), 4, 24)


def make_key_222(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_4(strings) + 'xx46'), 3, 24)


def make_key_223(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_19(strings) + 'xx47'), 4, 24)


def make_key_224(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_0(strings) + 'xx48'), 3, 24)


def make_key_225(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_1(strings) + 'xx49'), 4, 24)


def make_key_226(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_4(strings) + 'xx50'), 3, 24)


def make_key_227(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'xx51'), 4, 24)


def make_key_228(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_15(strings) + 'xx52'), 1, 24)


def make_key_229(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_16(strings) + 'wsn53'), 2, 24)


def make_key_230(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_0(strings) + 'wsn54'), 1, 24)


def make_key_231(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'wsn55'), 2, 24)


def make_key_232(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'wsn56'), 3, 24)


def make_key_233(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings) + 'wsn57'), 4, 24)


def make_key_234(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_3(strings) + 'wsn58'), 1, 24)


def make_key_235(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_19(strings) + 'wsn59'), 2, 24)


def make_key_236(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_0(strings) + 'wsn60'), 3, 24)


def make_key_237(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_1(strings) + 'c5a22'), 2, 24)


def make_key_238(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_4(strings) + 'c5a23'), 3, 24)


def make_key_239(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_5(strings) + 'c5a24'), 1, 24)


def make_key_240(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'c5a25'), 2, 24)


def make_key_241(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_7(strings) + 'c5a26'), 3, 24)


def make_key_242(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings) + 'c5a27'), 4, 24)


def make_key_243(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_7(strings) + 'c5a28'), 1, 24)


def make_key_244(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_8(strings) + 'c5a29'), 2, 24)


def make_key_245(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_14(strings) + 'c5a30'), 3, 24)


def make_key_246(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_15(strings) + 'c5a31'), 4, 24)


def make_key_247(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_16(strings) + 'c5a32'), 1, 24)


def make_key_248(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_9(strings) + 'c5a33'), 2, 24)


def make_key_249(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_10(strings) + 'c5a34'), 3, 24)


def make_key_250(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_17(strings) + 'c5a35'), 4, 24)


def make_key_251(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_1(strings) + 'f1b'), 3, 24)


def make_key_252(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_2(strings) + 'f2b'), 4, 24)


def make_key_253(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_3(strings) + 'f3b'), 1, 24)


def make_key_254(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'f4b'), 2, 24)


def make_key_255(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_5(strings) + 'f5b'), 1, 24)


def make_key_256(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_6(strings) + 'f6b'), 2, 24)


def make_key_257(strings):
    return sub_str(hex_md5(make_key_14(strings) + make_key_7(strings) + 'c5a17'), 3, 24)


def make_key_258(strings):
    return sub_str(hex_md5(make_key_15(strings) + make_key_8(strings) + 'c5a18'), 4, 24)


def make_key_259(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_9(strings) + 'c5a19'), 1, 24)


def make_key_260(strings):
    return sub_str(hex_md5(make_key_9(strings) + make_key_10(strings) + 'c5a20'), 2, 24)


def make_key_261(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_11(strings) + 'c5a21'), 3, 24)


def make_key_262(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_12(strings) + 'c5a22'), 2, 24)


def make_key_263(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_13(strings) + 'c5a23'), 3, 24)


def make_key_264(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_14(strings) + 'c5a24'), 4, 24)


def make_key_265(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_15(strings) + 'c5a25'), 1, 24)


def make_key_266(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_16(strings) + 'c5a28'), 2, 24)


def make_key_267(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_17(strings) + 'c5a29'), 3, 24)


def make_key_268(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_18(strings) + 'c5a30'), 4, 24)


def make_key_269(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_19(strings) + 'c5a31'), 1, 24)


def make_key_270(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_1(strings) + 'c5a32'), 2, 24)


def make_key_271(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_4(strings) + 'c5a33'), 3, 24)


def make_key_272(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_19(strings) + 'c5a34'), 4, 24)


def make_key_273(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_0(strings) + 'c5a35'), 3, 24)


def make_key_274(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_1(strings) + 'f1b'), 4, 24)


def make_key_275(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings) + 'f2b'), 1, 24)


def make_key_276(strings):
    return sub_str(hex_md5(make_key_7(strings) + make_key_5(strings) + 'f3b'), 2, 24)


def make_key_277(strings):
    return sub_str(hex_md5(make_key_16(strings) + make_key_5(strings) + 'f2b'), 1, 24)


def make_key_278(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_3(strings) + 'f3b'), 2, 24)


def make_key_279(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_3(strings) + 'f4b'), 3, 24)


def make_key_280(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_17(strings) + 'f5b'), 4, 24)


def make_key_281(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_18(strings) + 'f6b'), 1, 24)


def make_key_282(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_19(strings) + 'f7b'), 2, 24)


def make_key_283(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'f8b'), 3, 24)


def make_key_284(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'f9b'), 4, 24)


def make_key_285(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings) + 'f10b'), 3, 24)


def make_key_286(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings) + 'f11b'), 4, 24)


def make_key_287(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_1(strings) + 'f12b'), 1, 24)


def make_key_288(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_4(strings) + 'f13b'), 2, 24)


def make_key_289(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings) + 'f14b'), 1, 24)


def make_key_290(strings):
    return sub_str(hex_md5(make_key_10(strings) + make_key_0(strings) + 'f15b'), 2, 24)


def make_key_291(strings):
    return sub_str(hex_md5(make_key_17(strings) + make_key_1(strings) + 'f16b'), 3, 24)


def make_key_292(strings):
    return sub_str(hex_md5(make_key_18(strings) + make_key_10(strings) + 'f17b'), 4, 24)


def make_key_293(strings):
    return sub_str(hex_md5(make_key_19(strings) + make_key_17(strings) + 'f18b'), 1, 24)


def make_key_294(strings):
    return sub_str(hex_md5(make_key_0(strings) + make_key_18(strings) + 'f19b'), 2, 24)


def make_key_295(strings):
    return sub_str(hex_md5(make_key_1(strings) + make_key_19(strings) + 'f20b'), 3, 24)


def make_key_296(strings):
    return sub_str(hex_md5(make_key_4(strings) + make_key_0(strings) + 'f21b'), 4, 24)


def make_key_297(strings):
    return sub_str(hex_md5(make_key_5(strings) + make_key_1(strings) + 'f22b'), 3, 24)


def make_key_298(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_4(strings) + 'f23b'), 4, 24)


def make_key_299(strings):
    return sub_str(hex_md5(make_key_3(strings) + make_key_5(strings) + 'f24b'), 1, 24)


def get_vl5x(vjkl5, logger):
    """
    calculate vl5x vy vjkl5
    :param vjkl5:
    :param logger:
    :return:
    """
    func_len = 300
    num = int(str2long(vjkl5))
    index = num % func_len
    call_func = 'make_key_{}("{}")'.format(index, vjkl5)
    logger.info('begin to excute func {}'.format(call_func))
    res = eval(call_func)
    return res