from scrapy.cmdline import execute
spiders = [
    'scrapy crawl weibospider',
]
 
if __name__ == '__main__':
    for i in spiders:
        execute(i.split())


