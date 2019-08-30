#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.utils.phantom import get_web_driver
from ics.utils.logger_util import get_custom_task_logger
from ics.utils.string_tool import is_json

get_web_driver = get_web_driver
get_ics_logger = get_custom_task_logger
is_json = is_json
