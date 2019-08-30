#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/4
"""
import json
import time
import random
from ics.scheduler import app
from ics.utils.md5_tool import to_md5
from ics.utils.decorator import stable2
from ics.scheduler.new_task import StableTask
from ics.http.http_downloader import Downloader
from ics.task.zgcpws.batch.batch_dao import *
from ics.task.zgcpws_app.cdrcb.decrypt_tool import dec_aes_content

lst_change_ip = list()

lst_change_ip.append(('<span>360安域</span>'))


def app_judge_func(resp, meta):
    if resp.content == "":
        return True
    for cont in lst_change_ip:
        if cont in resp.content:
            return True
    return False


def app_solution_func(resp, meta):
    update_token()
    update_header()

    data = json.loads(meta["data"])
    data["reqtoken"] = token
    data = str(json.dumps(data, ensure_ascii=False))

    download_app.requests_param["headers"] = header
    download_app.requests_param["data"] = data

    download_app.change_add_grey_proxy()

    logger.warn('update hearder,token and change_add_grey success!!!')


download_app = Downloader(spider_no='zgcpws_app', logger=logger, abandon_model="grey",grey_time=3,session_keep=False, headers_mode=1, proxy_strategy=0, proxy_mode="dly")

download_app.set_retry_solution(app_judge_func, app_solution_func)

device_id = ''
token = ''
header = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; LLD-AL30 Build/HONORLLD-AL30)',
    'Content-Type': 'application/json',
    'Connection': 'Keep-Alive',
    'Host': 'wenshuapp.court.gov.cn'
}
device_cnt = 0


def get_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def get_nonce():
    seed = "abcdefghijklmnopqrstuvwxyz0123456789"
    sa = []
    for i in range(4):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def update_device_id():
    global device_id
    md5_str = get_time()
    char_str = 'abcdefghijklmnopqrstuvwxyz'
    tail = random.randint(1, 14)
    for i in range(tail):
        md5_str += random.choice(char_str)
    device_id = to_md5(md5_str)


def get_signature(timespan, nonce):
    global device_id
    lists = [timespan, nonce, device_id]
    lists.sort()
    value = ''.join(lists)
    return to_md5(value)


def update_token():
    global device_id
    global token

    data = {"devid": device_id, "apptype": "1", "app": "cpws"}
    url = 'http://wenshuapp.court.gov.cn/MobileServices/GetToken'
    update_header()
    req = download_app.post(url, json=data, headers=header, retry_cnt=8, time_out=20).json()
    token = req.get('token')


def update_header():
    global device_id
    global device_cnt
    if device_cnt >= 30:
        device_cnt += 1
        update_device_id()
        device_cnt = 0
    nonce = get_nonce()
    timespan = get_time()
    signature = get_signature(timespan, nonce)
    temp_header = {'devid': device_id,
                   'nonce': nonce,
                   'signature': signature,
                   'timespan': timespan}
    header.update(temp_header)


@app.task(bind=True, base=StableTask, default_retry_delay=0.5, max_retries=5, ignore_result=True)
@stable2(Exception, logger=logger)
def start_with_doc_id(self, doc_id):
    global device_id
    global token
    global header

    if not device_id or not token:
        update_device_id()
        update_token()

    app_url = 'http://wenshuapp.court.gov.cn/MobileServices/GetAllFileInfoByIDNew'
    update_header()
    # print(header)
    data = {"fileId": doc_id,
            "app": "cpws",
            "reqtoken": token
            }
    data = str(json.dumps(data, ensure_ascii=False))

    meta = {"header": header, "data": data}
    time.sleep(random.randint(2, 4) * 0.5)
    req = download_app.post(app_url, data=data, headers=header, retry_cnt=8, time_out=20, meta=meta).content
    if "非授权使用" in req:
        raise Exception("非授权使用 in response")

    dec_cont = dec_aes_content(token, header["timespan"], req, header["devid"])
    result_dic = add_key(doc_id, dec_cont)
    save_data(result_dic, logger)
    update_status(result_dic.get("doc_id"), logger)