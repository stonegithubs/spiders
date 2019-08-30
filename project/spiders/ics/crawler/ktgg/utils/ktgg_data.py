#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:ktgg_data.py
author:mjw
version: 1.0
date:2018-09-29-11:50
"""


class KtggData(object):
    def __init__(self):
        self.ename = None  # 开庭公告域名标识
        self.domain = None  # 开庭公告域名标识
        self.cname = None  # 开庭公告中文名称
        self.unique_id = None  # 唯一标识
        self.title = None  # 标题
        self.body = None  # 正文
        self.court = None  # 法院
        self.court_room = None  # 法庭
        self.court_date = None  # 开庭日期
        self.case_number = None  # 案号
        self.case_cause = None  # 案由
        self.undertake_dept = None  # 承办部门
        self.undertake_person = None  # 承办人/承办法官
        self.court_member = None  # 合议庭/合议庭成员
        self.court_clerk = None  # 书记员
        self.responsible_court = None  # 承办法院
        self.presiding_judge = None  # 主审
        self.chief_judge = None  # 审判长
        self.judiciary = None  # 审判员
        self.prosecutor = None  # 原告
        self.defendant = None  # 被告
        self.party = None  # 当事人
        self.case_introduction = None  # 案情简介
        self.province = None  # 省
        self.url = None  # URL地址
        self.raw_id = None  # 原文id
        self.created_at = None  # 抓取时间

    def to_dict(self):
        return self.__dict__
