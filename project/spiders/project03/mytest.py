import requests

resp = requests.get("https://list.jd.com/list.html?cat=1713,3260,3340&tid=3340")
content = resp.content

with open("./xx.html","wb") as file:
    file.write(content)