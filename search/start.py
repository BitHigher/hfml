#!/usr/bin/python

import crawler
c = crawler.crawler("nju.db")
c.createtables()
c.crawl(['http://www.nju.edu.cn/'], 4)
