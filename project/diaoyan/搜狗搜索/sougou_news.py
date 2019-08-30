from lxml import etree
from newspaper import Article
import requests

url = 'https://news.sogou.com/news?query=%CF%E3%B8%DB'
res = requests.get(url).text
res = etree.HTML(res)
news_url_list = res.xpath('//div[@class="results"]/div[@class="vrwrap"]//h3//@href')
for i in news_url_list:
    news = Article(i, language='zh')
    news .download()
    news .parse()
    print(1,news.text)
    print(2,news.title)
    # print(news.html)
    # print(3,news.authors)
    # print(4,news.top_image)
    # print(5,news.movies)
    # print(6,news.keywords)
    # print(7,news.summary)