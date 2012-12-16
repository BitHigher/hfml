#!/usr/bin/python

import urllib2

#stocks = [
#	'YHOO', 'AVP', 'BIIB', 'BP', 'CL', 'CVX',
#	'XOM', 'EXPE', 'GOOG', 'INTC', 'PG', 'MSFT'
#]

stocks = [
	'FB', 'BIDU'
]

for stock in stocks:
	data = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=' + stock + 
							'&d=11&e=15&f=2012&g=d&a=6&b=9&c=1986&ignore=.csv')

	f = open(stock, 'w')
	f.write(data.read())
	f.flush()
	f.close()
	print stock, ' downloaded'

