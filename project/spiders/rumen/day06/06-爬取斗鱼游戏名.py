import requests

resp = requests.get('https://webconf.douyucdn.cn/resource/common/activity/act201810_w.json')
resp = resp.content.decode()
with open('./游戏名字.json', 'w')as f:
    f.write(resp)
