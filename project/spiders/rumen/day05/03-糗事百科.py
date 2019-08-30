# import csv
# import requests
# from lxml import etree
#
#
# class QiuBaiSpaider:
#     """糗百爬虫"""
#
#     def __init__(self):
#         self.url_temp = 'https://www.qiushibaike.com/8hr/page/{}/'
#         self.headers = {
#             'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
#         }
#         self.flag = True
#
#     def get_url_list(self):
#         """获取url列表"""
#         return [self.url_temp.format(i) for i in range(1, 14)]
#
#     def parse_url(self, url):
#         """发送请求"""
#         try:
#             response = requests.get(url, headers=self.headers)
#             return response.content.decode("utf-8")
#         except Exception as ex:
#             print(ex)
#             return ""
#
#     def get_page_content_list(self, html_str):
#         """提取每一页数据"""
#         html = etree.HTML(html_str)
#         div_list = html.xpath('//div[@id="content-left"]/div')  # 分组
#         content_list = []
#         for div in div_list:
#             item = {}
#             item['content'] = ''.join(div.xpath('/a/div/span/text()')).replace('\n',
#                                                                                '')  # .//div[@class='content']/span/text()
#         return content_list
#
#     def save_page_content_list(self, content_list):
#         """保存数据"""
#         if self.flag:
#             keys = content_list[0].keys()
#             values = [i.values() for i in content_list]
#             with open('./files/糗事百科.csv', 'a')as file:
#                 csv_writer = csv.writer(file)
#                 csv_writer.writerow(keys)
#                 csv_writer.writerows(values)
#             self.flag = False
#         else:
#             values = [i.values() for i in content_list]
#             with open("./files/臭事百科.csv", "a", encoding="utf-8") as file:
#                 csv_writer = csv.writer(file)
#                 csv_writer.writerows(values)
#
#     def run(self):
#         # 1.url_list
#         url_list = self.get_url_list()
#
#         # 2.发送请求,获取响应
#         for url in url_list:
#             html_str = self.parse_url(url)
#             # 3.提取数据
#             content_list = self.get_page_content_list(html_str)
#             # 2.保存
#             self.save_page_content_list(content_list)
#
#
# if __name__ == '__main__':
#     qiubai = QiuBaiSpaider()
#     qiubai.run()
# # # //div[@class="author clearfix"]/a/h2/text()  # 用户名
# #
# # response = requests.get(url, headers=headers)
# # response = response.content.decode()
# #
# # all_data = []
# #
# # resp = etree.HTML(response)
# # # //div[@class="article block untagged mb15 typs_long"]//div[@class="content"]/span/text()
# # res = resp.xpath('//div[@id="content-left"]')
# # # //div[@id="content-left"]   /div/div[@class="author clearfix"]/a/h2/text()
# # for i in res:
# #     data = {}
# #     # data['uname'] = i.xpath('.//div[@class="author clearfix"]//h2/text()')[0].strip()
# #     data['uname'] = ''.join(i.xpath('.//div[@class="author clearfix"]//h2/text()')).replace('\n','')
# #     data['ucontent'] = ''.join(i.xpath('./div/a/div/span/text()')).replace('\n','')
# #     print(data['uname'] + '\n' + data['ucontent'] + '\n\n')
# #     all_data.append(data)
# #
# # print(all_data)





import requests
from lxml import etree
import csv


class QiubaiSpdier:
    """臭事百科爬虫"""

    def __init__(self):
        """初始化参数"""
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
        self.flag = True

    def get_url_list(self):
        """获取url列表，总13页"""
        return [self.url_temp.format(i) for i in range(1, 14)]

    def parse_url(self, url):
        """解析url"""
        try:
            response = requests.get(url, headers=self.headers)
            return response.content.decode("utf-8")
        except Exception as ex:
            print(ex)
            return ""

    def get_page_content_list(self, html_str):
        """提取每一页的数据"""
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@id='content-left']/div")  # 分组
        content_list = []
        for div in div_list:
            item = {}
            item["content"] = "".join(div.xpath(".//div[@class='content']/span/text()")).replace("\n", "")
            item["author_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
            item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon", "") if len(
                item["author_gender"]) > 0 else None
            item["auhtor_age"] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
            item["auhtor_age"] = item["auhtor_age"][0] if len(item["auhtor_age"]) > 0 else None
            item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")
            item["content_img"] = "https:" + item["content_img"][0] if len(item["content_img"]) > 0 else None
            item["author_img"] = div.xpath(".//div[@class='author clearfix']//img/@src")
            item["author_img"] = "https:" + item["author_img"][0] if len(item["author_img"]) > 0 else None
            item["stats_vote"] = div.xpath(".//span[@class='stats-vote']/i/text()")
            item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else None
            content_list.append(item)
        return content_list

    def save_page_content_list(self, content_list):  # [{},{},{}]
        """保存数据"""

        if self.flag:
            keys = content_list[0].keys()
            values = [i.values() for i in content_list]
            with open("./files/臭事百科.csv", "a", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(keys)
                csv_writer.writerows(values)
            self.flag = False
        else:
            values = [i.values() for i in content_list]
            with open("./files/臭事百科.csv", "a", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(values)

    def run(self):
        """主要逻辑"""

        # 1.url_list
        url_list = self.get_url_list()
        # 2.遍历，发送请求，获取响应
        for url in url_list:
            html_str = self.parse_url(url)
            # 3.提取数据
            content_list = self.get_page_content_list(html_str)
            # 4.保存
            self.save_page_content_list(content_list)
            # break


if __name__ == '__main__':
    qiubai = QiubaiSpdier()
    qiubai.run()
