#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import sys
import base64
from Crypto.Cipher import AES
from ics.utils.md5_tool import to_md5
from ics.utils.string_tool import abstract
from ics.utils.html import clear_noise

reload(sys)
sys.setdefaultencoding('utf-8')


def get_index(token):
    temp = long(str2long_a(token, 1))
    return temp % 20


def str2long_a(strings, step):
    long_str = 0
    for index in range(len(strings)):
        long_str += (index + step) + (ord(strings[index]) << (index & 7)) - ord(strings[index])
    return str(long_str)


def str2long_b(strings, step):
    long_str = 0
    for index in range(len(strings)):
        long_str += (ord(strings[index]) << (index % 16)) + (index + step - ord(strings[index]))
    return str(long_str)


def str2long_c(strings, step):
    long_str = 0

    for index in range(len(strings)):
        long_str += (index + step) + (ord(strings[index]) << (index % 16)) + index % 4 - ord(strings[index])
    return str(long_str)


def get_key_e(token):
    v3 = 39
    v0 = to_md5(token[5:30] + token[36:v3])[4:20]
    return v0


def get_key_f(token):
    v5 = 39
    v2 = 5
    v4 = 4
    v3 = 3
    v0 = token[v2:30] + "5" + token[1:v3] + "1" + token[36:v5]
    v0 = to_md5(v0[v4:] + (v0[v2:] + v0[v4:])[v3:])[6:22]
    return v0


def get_key_q(arg7):
    v5 = 39
    v2 = 5
    v4 = 4
    v0 = arg7[v2:30] + arg7[1: 3] + "1" + arg7[36: v5]
    v0 = to_md5(v0[v4:] + to_md5((v0[v2:] + v0[v4:])[6:]))[1:17]
    return v0


def get_key_r(arg8):
    v2 = 39
    v4 = 5
    v0 = arg8[v4:30] + arg8[36: v2]
    v0 = to_md5(str2long_b(v0[4:], v4) + (v0[v4:] + v0[7:])[1:])[1: 17]
    return v0


def get_key_s(arg8):
    v2 = 39
    v3 = 4
    v6 = 2
    v0 = arg8[v6: 27] + arg8[36: v2]
    v0 = to_md5(str2long_a(v0[v3:], 13) + (v0[12:] + v0[v3:])[v6:])[1: 17]
    return v0


def get_key_t(arg7):
    v2 = 39
    v4 = 4
    v3 = 2
    v0 = arg7[v3:27] + arg7[36: v2]
    v0 = to_md5(str2long_a(v0[v4:], v3) + (v0[12:] + v0[v4:])[v3:])[3: 19]
    return v0


def get_key_u(arg8):
    v2 = 33
    v3 = 4
    v6 = 2
    v0 = arg8[v6:27] + arg8[30:v2]
    v0 = to_md5(str2long_b(v0[v3:], 3) + (v0[1:] + v0[v3:])[v6:])[10: 26]
    return v0


def get_key_v(token):
    v2 = 39
    v7 = 6
    v6 = 2
    v0 = token[v6:27] + token[36:v2]
    v0 = to_md5(str2long_c(v0[v6:], 11) + (v0[v6:] + v0[v7:12])[v6:])[v7:22]
    return v0


def get_key_w(arg8):
    v2 = 39
    v3 = 4
    v6 = 2
    v0 = arg8[v6: 27] + arg8[36: v2]
    v0 = to_md5(str2long_a(v0[v3:], 13) + base64.b64encode(v0[12:] + v0[v3:])[v6:])[1: 17]
    return v0


def get_key_x(token):
    v2 = 39
    v4 = 4
    v3 = 2
    v0 = token[v3:27] + token[36:v2]
    v0 = to_md5(base64.b64encode(v0[v4:]) + (v0[12:] + v0[v4:])[v3:])[7:23]
    return v0


def get_key_g(token):
    v2 = 27
    v0 = to_md5(token[5:v2] + token[12:15])[9:25]
    return v0


def get_key_h(token):
    v5 = 39
    v4 = 4
    v3 = 3
    v0 = token[5:30] + "5whq" + token[1: v3] + "1" + token[36: v5]
    v0 = to_md5(v0[v4:] + (v0[10:] + v0[v4:])[v3:])[6: 22]
    return v0


def get_key_i(arg7):
    v5 = 39
    v2 = 5
    v3 = 4
    v0 = arg7[v2: 30] + arg7[1: 3] + "1" + arg7[36: v5]
    v0 = to_md5(v0[v3:] + str2long_c((v0[v2:] + v0[v3:])[6:], 45))[1: 17]
    return v0


def get_key_j(arg7):
    v3 = 39
    v2 = 5
    v0 = arg7[v2:30] + arg7[36: v3]
    v0 = to_md5(to_md5(v0[4:] + "5") + (v0[v2:] + v0[7:])[1:])[1: 17]
    return v0


def get_key_k(arg8):
    v4 = 4
    v6 = 27
    v3 = 2
    v0 = arg8[v3: v6] + arg8[16: 19]
    v0 = to_md5(str2long_b(v0[v4:], v3) + (v0[12:] + v0[v4:])[v3:])[11:v6]
    return v0


def get_key_l(arg7):
    v2 = 39
    v4 = 4
    v3 = 2
    v0 = arg7[v3: 27] + arg7[36: v2]
    v0 = to_md5(str2long_c(v0[v4:], v3) + (v0[12:] + v0[v4:])[v3:])[3: 19]
    return v0


def get_key_m(arg8):
    str1 = arg8[2: 27] + arg8[30: 33]
    arrayOfByte = (str1[12:] + str1[4:])[2:]
    return to_md5(str2long_b(str1[4:], 1) + base64.b64encode(arrayOfByte))[1: 17]


def get_key_n(paramString):
    str1 = paramString[2: 27] + paramString[36: 39]
    arrayOfByte = (str1[2:] + str1[6:12])[12:]
    return to_md5(str2long_c(str1[2:], 11) + base64.b64encode(arrayOfByte))[3:19]


def get_key_o(paramString):
    str1 = paramString[2:27] + paramString[36: 39]
    str2 = base64.b64encode(str1[10:] + "a2aaa" + str1[4:])
    return to_md5(str2long_a(str1[4:] + "f4v6", 13) + str2[2:])[1: 17]


def get_key_p(paramString):
    str1 = paramString[2: 27] + "a2daa" + paramString[36: 39]
    str2 = str1[12:] + str1[4:]
    arrayOfByte = str1[4:]
    return to_md5(base64.b64encode(arrayOfByte) + str2[2:])[7: 23]


def dec_aes(token, timespan, content, dev_id):
    key = get_dec_key(token, timespan)
    iv = dev_id[-16:]
    PADDING = b"\x0b"
    generator = AES.new(key, AES.MODE_CBC, iv)
    recovery = generator.decrypt(base64.b64decode(content))
    recovery = recovery.rstrip(PADDING).replace('\n', '').replace('\r', '')
    recovery = '[' + abstract(recovery, '[', ']') + ']'
    return recovery


def get_func_lst():
    func_lst = list()
    func_lst.append(get_key_e)
    func_lst.append(get_key_f)
    func_lst.append(get_key_q)
    func_lst.append(get_key_r)
    func_lst.append(get_key_s)
    func_lst.append(get_key_t)
    func_lst.append(get_key_u)
    func_lst.append(get_key_v)
    func_lst.append(get_key_w)
    func_lst.append(get_key_x)
    func_lst.append(get_key_g)
    func_lst.append(get_key_h)
    func_lst.append(get_key_i)
    func_lst.append(get_key_j)
    func_lst.append(get_key_k)
    func_lst.append(get_key_l)
    func_lst.append(get_key_m)
    func_lst.append(get_key_n)
    func_lst.append(get_key_o)
    func_lst.append(get_key_p)
    return func_lst


def get_dec_key(token, timespan):
    func_lst = get_func_lst()
    index = get_index(token)
    dec_key = func_lst[index](token + timespan)
    return dec_key

def dec_aes_content(token, timespan, content, dev_id):
    key = get_dec_key(token, timespan)
    iv = dev_id[-16:]
    generator = AES.new(key, AES.MODE_CBC, iv)
    recovery = generator.decrypt(base64.b64decode(content))
    return recovery