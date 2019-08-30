import requests


url = 'https://cdn4.buysellads.net/uu/1/3386/1525189943-38523.png'
r = requests.get(url=url)

with open('./images/02.png', 'wb') as f:
    f.write(r.content)
