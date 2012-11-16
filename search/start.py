#!/usr/bin/python

import crawler
c = crawler.crawler("cnbeta.db")
c.createtables()
c.crawl(['http://cnbeta.com/'], 4)
