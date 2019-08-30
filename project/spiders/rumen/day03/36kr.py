import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
b_id = 143860

while True:
    url = 'https://36kr.com/api/newsflash?b_id={}'.format(b_id)

    response = requests.get(url=url, headers=headers)
    b_id = b_id - 20
    print(url)
    resp = response.content.decode()
    # print(resp)
    # resp = json.loads(resp)

    # res = re.findall(r"<script>var props=(.*?),locationnal=", resp)[0]
    res = json.loads(resp)
    for i in range(len(res['data']['items'])):
        ret = res['data']['items'][i]['title']
        ref = res['data']['items'][i]['description']
        print(ret)
        with open('../files/36kr-news.txt', 'a')as f:
            f.write(ret + '\n' + ref + '\n\n')
