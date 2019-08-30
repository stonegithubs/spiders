import json

from parse_url import parse_url

search_str = input('要搜索内容:')
url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=530&salary=8001,10000&workExperience=-1&education=5&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3&lastUrlQuery=%7B%22jl%22:530,%22sf%22:%228001%22,%22st%22:%2210000%22,%22el%22:%225%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D&_v=0.34189574&x-zp-page-request-id=08ffabd0d35747dba1f31be44878ee72-1541400241972-778310'.format(search_str)
# url = 'https://sou.zhaopin.com/?jl=538&sf=8001,10000&st=10000&el=5&kw=python&kt=3'
content_str = parse_url(url)
# print(content_str)
content_str = json.loads(content_str)

# print(len(content_str['data']['results']))

# 写入前清空文件内容
# with open('./zhilian.txt', 'w', encoding='utf8')as f:
#     f.write('')

for i in range(len(content_str['data']['results'])):
    res = content_str['data']['results'][i]['company']['name']  # 公司名
    ret = content_str['data']['results'][i]['jobName']  # 职位名
    ref = content_str['data']['results'][i]['salary']  # 薪资
    print('公司名:' + res + '\t' + '岗位:' + ret + '\t' + '薪资:' + ref)

    # with open('./zhilian.txt', 'a', encoding='utf8')as f:
    #     f.write('公司名:' + res + '\t' + '岗位:' + ret + '\t' + '薪资:' + ref + '\n')
