import requests
from retrying import retry

header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', }


@retry(stop_max_attempt_number=4)
def _parse_url(url, method, data, proxies):
    # print('*')
    if method == 'POST':
        r = requests.post(url, data=data, proxies=proxies)
    else:
        r = requests.get(url, data=data, proxies=proxies)
    assert r.status_code == 200
    return r.content.decode()


def parse_url(url, method='GET', data=None, proxies={}):
    try:
        html_str = _parse_url(url, method, data, proxies)
    except:
        html_str = None

    return html_str


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    print(parse_url(url))
