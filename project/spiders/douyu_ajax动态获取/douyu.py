import requests
import json


def open_html(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.text


def run():
    a = 1
    # 直播间最多数量
    sum = 600
    # 去除重复的直播间id
    Hashfilter = {}
    # 存放数据
    data_list = []
    # 爬去数量
    count = 0

    while a <= sum:
        # 页码数
        page_num = 1
        # 开始url
        start_url = 'https://www.douyu.com/gapi/rkc/directory/2_40/' + str(page_num)
        # 发送请求
        html = open_html(start_url)
        json_data = json.loads(html)
        page_nums = json_data['data']['pgcnt']
        while page_num <= page_nums:
            start_url = 'https://www.douyu.com/gapi/rkc/directory/2_40/' + str(page_num)
            html = open_html(start_url)
            json_data = json.loads(html)
            for data in json_data['data']['rl']:
                rid = str(data['rid'])
                item = {}
                if rid not in Hashfilter:
                    Hashfilter[rid] = True
                    item['user_name'] = data['nn']
                    item['room_name'] = data['rn']
                    item['room_num'] = data['rid']
                    item['host_num'] = data['ol']
                    item['game_name'] = data['c2name']
                    data_list.append(item)
                    count += 1
                    print('正在爬取%s的第：%s条数据' % (item['game_name'], count))
                else:
                    break
            page_num += 1

        print(data_list)


run()

