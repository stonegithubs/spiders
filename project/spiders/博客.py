import threading
import requests
from queue import Queue
import time


class BoKe(object):

    def __init__(self, callback_url, resp_url):
        self.url_temp = callback_url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': resp_url
        }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.ok_content = 0
        self.time_start = time.time()

    def get_url_list(self):
        """获取url列表"""
        for i in range(100):
            # 每次循环放进100个url
            self.url_queue.put(self.url_temp)

    def parse_url(self):
        while True:
            # 取出url
            url = self.url_queue.get()
            # 请求url
            resp = requests.get(url, headers=self.headers)
            # 如果状态码等于200
            if resp.status_code == 200:
                # 请求成功次数+1
                self.ok_content +=1
            self.url_queue.task_done()

    def run(self):
        """主函数"""
        # 进程列表
        thread_list = []
        for i in range(10):  # 单位百
            # 创建10个进程
            t_url = threading.Thread(target=self.get_url_list)
            thread_list.append(t_url)
        for i in range(20):
            # 创建50个进程
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)

        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程,该线程不重要,主线程结束,子线程结束.
            t.start()  # 启动进程

        for q in [self.url_queue, self.html_queue]:
            q.join()  # 让主线程等待阻塞,等待队列的任务完成之后再完成
        time_end = time.time()
        print('用时:%.2f秒'% (time_end - self.time_start ))
        print('新增访客量:', self.ok_content)
        print('主线程结束')


if __name__ == '__main__':
    callback_url = 'https://busuanzi.ibruce.info/busuanzi?jsonpCallback={}'.format('BusuanziCallback_1065646564382')
    boke_url = 'https://yuye.work/2017/05/22/006%E9%AA%8C%E8%AF%81%E7%A0%81%E4%B8%8Eselenium/'
    boke = BoKe(callback_url, boke_url)
    boke.run()
