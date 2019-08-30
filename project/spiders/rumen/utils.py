import re

with open('./utils.txt', 'r', encoding='utf-8') as file:
    headers = file.read()
    # headers = "Host: www.baidu.com"
    new = re.sub('(.*?):\s(.*)', lambda m: "\'" + m.group(1) + "\': \'" + m.group(2) + "\',", headers)
    print('{\n' + new + '\n}')
