import json
import requests


class BoosGetCity(object):
    """类"""
    def __init__(self):
        """初始化"""
        self.url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'

    def run(self):
        """主函数"""
        res = requests.get(self.url).text
        res = json.loads(res)
        city_list = res['zpData']['cityList']
        # print(city_list)
        for i in city_list:
            detail_city_list = i['subLevelModelList']
            for j in detail_city_list:
                print(j)
                with open('citys_code.txt','a',encoding='utf8')as f:
                    f.write(str(j['code'])+'\n')


if __name__ == '__main__':
    boos = BoosGetCity()  # 创建对象
    boos.run()  # 调用函数
