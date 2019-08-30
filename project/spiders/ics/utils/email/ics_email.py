#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:send_email.py
description:
author:crazy_jacky
version: 1.0
date:2018/8/9
"""
import os
import sys
import smtplib

from email.header import Header
from email.mime.text import MIMEText
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from ics.utils import get_ics_logger
from ics.settings.default_settings import STMP_SERVER, SEND_FROM, SEND_TO, LOGIN_CODE

reload(sys)

sys.setdefaultencoding('utf-8')

logger = get_ics_logger(__name__)


class Send_Email(object):
    """
    send mail
    """

    def __init__(self, theme):
        self.server = smtplib.SMTP_SSL()
        self.server.connect(STMP_SERVER, 465)
        self.theme = theme
        self.server.login(SEND_FROM, LOGIN_CODE)

    def send_mail(self, text):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = SEND_FROM
        msg['To'] = SEND_TO
        msg['Subject'] = Header(self.theme, 'utf-8')
        self.server.sendmail('zheng_qipeng@icekredit.com', SEND_TO.split(';'), msg.as_string())
        self.server.quit()
