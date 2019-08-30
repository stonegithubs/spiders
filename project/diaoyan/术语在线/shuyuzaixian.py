import requests


class ShuYuZaiXianSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

    def run(self):
        a = 1
        for i in range(0,1000,15):
            url = 'http://www.termonline.cn/list.jhtm?op=query&k=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&start={}&pageSize=15&sort=&resultType=0&conds%5B0%5D.key=all&conds%5B0%5D.match=1&conds%5B1%5D.val=&conds%5B1%5D.key=category&conds%5B1%5D.match=1&conds%5B2%5D.val=&conds%5B2%5D.key=subject_code&conds%5B2%5D.match=3&conds%5B3%5D.val=&conds%5B3%5D.key=publish_year&conds%5B3%5D.match=1&conds%5B0%5D.val=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD'
            res = requests.get(url.format(i),self.headers).text
            print(a)
            a+=1
            print(res)


if __name__ == '__main__':
    shuyu = ShuYuZaiXianSpider()
    shuyu.run()
