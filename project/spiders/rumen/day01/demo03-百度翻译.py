import requests
import json
import sys


# query_string = sys.argv[1]
#
#
# def fanyi():
#     headers = {
#         'User-Agent'  : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', }
#
#     post_data = {
#         'query': query_string,
#         'from': 'zh',
#         'to': 'en',
#     }
#
#     post_url = 'https://fanyi.baidu.com/basetrans'
#     r = requests.post(url=post_url, data=post_data, headers=headers)
#     dict_ret = json.loads(r.content.decode())
#     ret = dict_ret['trans'][0]['dst']
#     print(query_string + ':' + ret)
#
#
# if __name__ == '__main__':
#     fanyi()


def fanyi():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', }
    query_string = str(input('输入要翻译的内容:'))
    lang = get_lang(query_string)
    if lang == 'zh':
        post_data = {
            'query': query_string,
            'from': 'zh',
            'to': 'en',
        }

    else:
        post_data = {
            'query': query_string,
            'from': 'en',
            'to': 'zh',
        }

    post_url = 'https://fanyi.baidu.com/basetrans'
    r = requests.post(url=post_url, data=post_data, headers=headers)
    dict_ret = json.loads(r.content.decode())
    ret = dict_ret['trans'][0]['dst']
    print(query_string + ':' + ret)


def get_lang(query_string):
    url = 'https://fanyi.baidu.com/langdetect'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', }
    data = {'query': query_string}
    r = requests.post(url=url, data=data, headers=headers)
    resp = json.loads(r.content.decode())
    res = resp['lan']
    return res


if __name__ == '__main__':
    fanyi()
