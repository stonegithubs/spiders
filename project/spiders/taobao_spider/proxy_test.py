import requests

start_url = 'http://www.baidu.com'
proxies = {
    'https': '183.148.139.249:9999'
}
resp = requests.get(start_url, proxies=proxies)
print(resp.status_code)
