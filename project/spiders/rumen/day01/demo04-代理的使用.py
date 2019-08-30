import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36', }

for i in range(15):
    with open('./ip.txt', 'r') as file:
        res = file.read()

    proxies = {'http': '{}'}.fromkeys(res)

    url = 'https://www.baidu.com'

    try:
        r = requests.get(url=url, headers=headers, proxies=proxies, timeout=3)
        print(i + 1, 'ok')
    except Exception:
        print('no')
