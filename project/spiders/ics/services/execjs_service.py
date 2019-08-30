#!/usr/bin/env python
#-*-coding:utf-8-*-


__author__ = 'wu_yong'

import os
import base64
import sys
import Queue
import json
import time
import traceback
import tornado.web
import tornado.ioloop
import tornado.httpserver
from retry import retry
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException
from ics.settings.default_settings import JS_SERVER_AUTH_USERNAME, JS_SERVER_AUTH_PASSWORD, JS_SERVER_CHROME_PATH

MAX_QUEUE_SIZE = 100
SERVER_PORT = 8888
WEB_RECV_QUEUE = Queue.Queue(maxsize=MAX_QUEUE_SIZE)
WEB_SEND_QUEUE = Queue.Queue(maxsize=MAX_QUEUE_SIZE)


logger = get_ics_logger('js_service')


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/execjs', ExcuteHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)


class STATUS(object):
    SUCCESS = 0
    FAILED = 1
    NO_DRIVER = 2
    NO_AUTH = 401


class ExcuteHandler(BaseHandler):

    @run_on_executor
    def post(self):
        result = {
            'status': STATUS.NO_AUTH,
            'msg': '',
            'result': '',
            'cost_time': 0,
        }
        authorization = self.request.headers.get('Authorization')
        js = self.get_argument('js')
        if self.verificat_auth(authorization) is True:
            self.exec_js(js, result)
        else:
            result['msg'] = 'permission denied'
            self.write(result)

    def verificat_auth(self, auth_header):
        if auth_header is not None:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            auth_username, auth_password = base64.b64decode(auth_base64).split(':', 1)
            if auth_username == JS_SERVER_AUTH_USERNAME and auth_password == JS_SERVER_AUTH_PASSWORD:
                return True

        self.set_status(STATUS.NO_AUTH)
        self.set_header('WWW-Authenticate', 'Basic permission denied')
        return False

    def exec_js(self, js, result):
        item = get_from_queue(WEB_RECV_QUEUE, 'WEB_RECV_QUEUE')
        if item is None:
            result['msg'] = u'no chrome can be used'
            result['status'] = STATUS.NO_DRIVER
        else:
            start_time = time.time()
            try:
                res = item['driver'].execute_script(js)
                msg = u'excute js success'
                result['status'] = STATUS.SUCCESS
                result['result'] = res
                item['status'] =STATUS.SUCCESS
            except Exception as e:
                msg = u'excute js failed, type e: {}, reasion: {}'.format(type(e), traceback.format_exc())
                result['status'] = STATUS.FAILED
                item['status'] = STATUS.FAILED
                item['err_cnt'] += 1
                logger.error(u'use chrome excute js failed, chrome info:{}'.format(item))

            result['msg'] = msg
            item['msg'] = msg
            item['use_cnt'] += 1
            WEB_SEND_QUEUE.put(item)
            end_time = time.time()
            cost_time = end_time - start_time
            result['order'] = item.get('order')
            result['cost_time'] = cost_time
        self.write(json.dumps(result, ensure_ascii=False))


@retry(exceptions=LogicException, tries=3, delay=0.5, logger=logger)
def get_driver():
    start_time = time.time()
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent= Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(executable_path=JS_SERVER_CHROME_PATH, chrome_options=chrome_options)
        end_time = time.time()
        logger.debug('generate driver success cost time:{}'.format(end_time - start_time))
        return driver
    except Exception:
        end_time = time.time()
        logger.debug('generate driver error cost time:{}'.format(end_time - start_time))
        raise LogicException(u'get_driver crate driver failed：e：{}'.format(traceback.format_exc()))


def package_new_driver(task_id, i):
    try:
        driver = get_driver()
    except:
        driver = None
    if driver is None:
        logger.info(u'generate the {} dirvier failed'.format(i))
        return
    msg_dict = {
        'use_cnt': 0,       # 破解次数
        'err_cnt': 0,
        'status': STATUS.SUCCESS,
        'msg': '',
        'driver': driver,   # dirvier obj
        'order': i,         # 序号
        'task_id': task_id,
    }
    WEB_RECV_QUEUE.put(msg_dict)
    logger.info(u'generate the {} drivier success and put to queue'.format(i))


def generate_driver_and_check(driver_cnt, task_id):
    for i in range(driver_cnt):
        try:
            package_new_driver(task_id, i)
        except Exception:
            raise LogicException(u'generate_driver 生成driver失败, i: {}, e：{}'.format(i, traceback.format_exc()))
    check_driver('task_1')


def get_from_queue(queue, queue_name, is_block=False):
    try:
        logger.debug(u'start get from {}, SEND_QUEUE qsize: {}, RECV_QUEUE qsize: {}'.\
                    format(queue_name, WEB_SEND_QUEUE.qsize(), WEB_RECV_QUEUE.qsize()))
        if is_block:
            item = queue.get()
        else:
            item = queue.get_nowait()
        logger.debug(u'get from {} success SEND_QUEUE qsize: {}, RECV_QUEUE qsize: {}'.\
                    format(queue_name, WEB_SEND_QUEUE.qsize(), WEB_RECV_QUEUE.qsize()))
        return item
    except Queue.Empty:
        pass


def check_driver(task_name):

    chrome_error_flag_list = [
        'Caused by NewConnectionError',
        'Failed to establish a new connection',
        'Connection refused',
    ]

    test_js = """
    function myFunction(a)
    {
       return 10*a;
    }
    """
    test_js = "return myFunction(2)"+test_js
    logger.info('start in thread_task: {}'.format(task_name))
    while True:
        try:
            item = get_from_queue(WEB_SEND_QUEUE, 'WEB_SEND_QUEUE', is_block=True)
            if item is None:
                continue
            if item['status'] == STATUS.FAILED:  # and item['err_cnt'] % 10 == 1:
                try:

                    # 对该chrome最近执行js的输出信息做一次自检，有问题，直接触发清理该chrome句柄和新生成动作
                    for err_str in chrome_error_flag_list:
                        if err_str in item.get('msg', ''):
                            err_msg = 'item msg contains error flag: {}'.format(item.get('msg'))
                            logger.info(err_msg)
                            raise Exception(err_msg)

                    test_js_val = item['driver'].execute_script(test_js)
                    if 20 == test_js_val:
                        logger.info(u'item:{} finish check，chrome normal'.format(item))
                        WEB_RECV_QUEUE.put(item)
                        logger.info(u'send to RECV_QUEUE success:{}'.format(item))
                    else:
                        logger.error(u'test js value is invalid, value:{}'.format(test_js_val))
                        raise Exception(u'chrome excute test js invalid, value: {}'.format(test_js_val))
                except Exception as e:
                    logger.error(u'检查chrome失败,chrome不可用,开始新增 driver exception:{}'.format(str(e)))
                    try:
                        logger.info(u'start clean up abandon driver, driver_info: {}'.format(item))
                        item['driver'].quit()
                        del item['driver']
                        logger.info(u'clean up abandon driver success, driver_info: {}'.format(item))
                    finally:
                        logger.info(u'create new chrome to relpace abandon chrome')
                        package_new_driver(item['task_id'], item['order'])
                        del item
            else:
                WEB_RECV_QUEUE.put(item)
                logger.info(u'send to RECV_QUEUE success:{}'.format(item))
        except:
            logger.error(u'check dirver error:{}'.format(traceback.format_exc()))


if __name__ == "__main__":
    exct = ThreadPoolExecutor(2)
    task1 = exct.submit(generate_driver_and_check, 5, 1)
    task2 = exct.submit(check_driver, 'task_2')
    logger.info(u'start in http_server......')
    app = App()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(port=SERVER_PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

