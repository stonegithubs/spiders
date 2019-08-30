from time import sleep
from threading import Thread
items = [2, 4, 5, 2, 1, 7]
def sleep_sort(i):
    sleep(i*0.001)
    print(i)

# [Thread.start_new_thread(sleep_sort,(i,)) for i in items]

import requests
ip = requests.get('http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=37176&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
ip = ip.text
print(ip)