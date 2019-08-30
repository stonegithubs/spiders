import requests

resp = requests.get('https://www.sina.com.cn/')
# 打印内容
# print(resp.text)
# 打印响应码
# print(resp.status_code)
# 获取url地址
# print(resp.url)
# print(resp.request.url)
print(resp.request.headers)
print(resp.headers)

# r = resp.content
# with open('./sina.html', 'wb') as file:
#     file.write(r)
