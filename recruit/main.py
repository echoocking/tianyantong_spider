# -*-coding: utf-8 -*-

from scrapy.cmdline import execute

# scrapy_spider為剛剛建立的spider name，可以在這裡切換不同的spider

execute(['scrapy', 'crawl', 'TianYanTong'])