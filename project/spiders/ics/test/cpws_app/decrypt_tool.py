#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'
from ics.utils.md5_tool import to_md5
import requests
import time
import base64
from Crypto.Cipher import AES
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')


# def str2long_a(token, i):
#     url = "http://{}:6688/jni?mth=a&str={}&i={}".format(host, token, i)
#     return requests.get(url).content
#
#
# def str2long_b(token, i):
#     url = "http://{}:6688/jni?mth=b&str={}&i={}".format(host, token, i)
#     return requests.get(url).content
#
#
# def str2long_c(token, i):
#     url = "http://{}:6688/jni?mth=c&str={}&i={}".format(host, token, i)
#     return requests.get(url).content


def get_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


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
    v0 = to_md5(token[5:v2] + token[12:15])[9:25];
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
    str1 = paramString[2, 27] + "a2daa" + paramString[36: 39]
    str2 = str1[12:] + str1[4:]
    arrayOfByte = str1[4:]
    return to_md5(base64.b64encode(arrayOfByte) + str2[2:])[7: 23]


def dec_aes(key, content, iv):
    PADDING = b"\x0b"
    generator = AES.new(key, AES.MODE_CBC, iv)
    recovery = generator.decrypt(base64.b64decode(content))
    recovery = recovery.rstrip(PADDING).replace('\n', '').replace('\r', '')
    return recovery


def get_nonce():
    seed = "abcdefghijklmnopqrstuvwxyz0123456789"
    sa = []
    for i in range(4):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def get_signature(timespan, nonce, device_id):
    lists = [timespan, nonce, device_id]
    lists.sort()
    value = ''.join(lists)
    return to_md5(value)


dec_list = list()
dec_list.append(get_key_e)
dec_list.append(get_key_f)
dec_list.append(get_key_q)
dec_list.append(get_key_r)
dec_list.append(get_key_s)
dec_list.append(get_key_t)
dec_list.append(get_key_u)
dec_list.append(get_key_v)
dec_list.append(get_key_w)
dec_list.append(get_key_x)
dec_list.append(get_key_g)
dec_list.append(get_key_h)
dec_list.append(get_key_i)
dec_list.append(get_key_j)
dec_list.append(get_key_k)
dec_list.append(get_key_l)
dec_list.append(get_key_m)
dec_list.append(get_key_n)
dec_list.append(get_key_o)
dec_list.append(get_key_p)


# host = "169.254.182.101"

token = "22c50c4dc0d36bcda49a292b841c006f"
timespan = "20180904142945"
content = "HFWn/eyUPWJG3aEy9PzohCaCtQ4v6qPEfA9qJOYMvmyuQq3+Eb2CeyjNvuw55Vn1TJfW9yKMJKVJBuYO3D3NST6da7/aYlh+2zeYmZJhNoWzRHBLpF8shea122q0dYBK/twhq0YTqSyY27uDE/fvO2VzlOnWEm72RR4gQ8UOVicGh/BCootryqRumMii5kSmWFAYlAo8vY1iCcAkxS8hfaz8QkB1pHM0JmL/qFUKgRr2BEdX4GsSKZ3EsGAeQTvGrEtcnYKLCDA1b4TBAmP30QMgYOM8BobuHfRYxMQXNLtrNwYwhbbNHP6XQEo7ykgaz5b2wLOBMjrPPx64gfmQWpYEK3v9VrCQpl1krMp5JYgonStmRUywrfv0prsBqbiLe4tbklaZjRRqHE9mtmVCij1xYeWU7ueGIyjwITyIT40FlgDpLnUqH3X48dqP35N+Q4y4IjjXBODVyayOekYEyHLmZYN33uHymNy7acQ57IqB8azXIgwQGZXTPVJDMKae7Q/H2DwFl3oOymQB2CqfK9PaTSSv+YwQ+yW3qYmo+hq9LnMoWrswmFoElg2vAb1/14L69jzB+bhwTvCU4+C3J+VmT6YuGaCUgkJjDr2iFbdccjtkz3rg87lHy4elIG+oDCFGnAUEeMZXaD02PfcRL0G5qnC/m3Ql+nQD4CfGgbo9zCkjPF8LVzWrLcCBPvGVSsg1JuV9nrYfFN06wuNWm9j8jvB4FHupje+Egwl3bGlPYXtiq9w/hDYbm1gAi7rhQHC8+tvNOt//CMqOjOoj2M57rROXT/QFFICdGn+hCTYh7nOH4GBJgbyXIzP18LtV810aur3sP6yu5cdjvqH5v48wA+JMt9QxpkBnNk+qNFyi3Bl/43pW8ROcSCtB5OTZAAXjsDWoT1xjU7Lw0vcvjg=="
iv = "84c722198d16fdcd"

index = get_index(token)

key = dec_list[index](token+timespan)

print dec_aes(key, content, iv)





