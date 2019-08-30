from bs4 import BeautifulSoup
from urllib import request
import chardet

from sqltest.MySQLCommand import MySQLCommand

url = "https://www.huxiu.com"
response = request.urlopen(url)
html = response.read()
charset = chardet.detect(html)
html = html.decode(str(charset["encoding"]))  # 设置抓取到的html的编码方式

# 使用剖析器为html.parser
soup = BeautifulSoup(html, 'html.parser')
# 获取到每一个class=hot-article-img的a节点
allList = soup.select('.hot-article-img')

# 连接数据库
mysqlCommand = MySQLCommand()
mysqlCommand.connectMysql()
#这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
dataCount = int(mysqlCommand.getLastId()) + 1
for news in allList:  # 遍历列表，获取有效信息
    aaa = news.select('a')
    # 只选择长度大于0的结果
    if len(aaa) > 0:
        # 文章链接
        try:  # 如果抛出异常就代表为空
            href = url + aaa[0]['href']
        except Exception:
            href = ''
        # 文章图片url
        try:
            imgUrl = aaa[0].select('img')[0]['src']
        except Exception:
            imgUrl = ""
        # 新闻标题
        try:
            title = aaa[0]['title']
        except Exception:
            title = ""

        #把爬取到的每条数据组合成一个字典用于数据库数据的插入
        news_dict = {
            "id": str(dataCount),
            "title": title,
            "url": href,
            "img_path": imgUrl
        }
        try:
            # 插入数据，如果已经存在就不在重复插入
            res = mysqlCommand.insertData(news_dict)
            if res:
                dataCount=res
        except Exception as e:
            print("插入数据失败", str(e))#输出插入失败的报错语句
mysqlCommand.closeMysql()  # 最后一定要要把数据关闭
dataCount=0