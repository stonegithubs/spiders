import re


def auto_headers():
    with open('./utils.txt', 'r', encoding='utf-8') as file:
        headers = file.read()
        new = re.sub('(.*?):\s(.*)', lambda m: "\'" + m.group(1) + "\': \'" + m.group(2) + "\',", headers)
        print('{\n' + new + '\n}')


def cookies():
    with open('./utils.txt', 'r', encoding='utf-8') as file:
        headers = file.read()
        for i in headers.split(';'):
            ii = re.sub('(.*?)=(.*)', lambda m: "\'" + m.group(1) + "\': \'" + m.group(2) + "\',", i)
            a = ii.replace(' ', '')
            print(a)

if __name__ == '__main__':
    auto_headers()  #自动headers
    # cookies()  # 自动cookies
