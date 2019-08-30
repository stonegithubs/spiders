from parse_url import parse_url
import re
import json

url = 'http://36kr.com/'
html_str = parse_url(url)

ret = re.findall('<script>var props=(.*),locationnal=', html_str)[0]
ret1 = re.findall('"template_title":"(.*?),"template_title_isSame"',ret)
for i in ret1:
    print(i)
    with open('./36kr.json', 'w', encoding='utf-8')as f:
        f.write(i)

ret = json.loads(ret)
print(ret)
