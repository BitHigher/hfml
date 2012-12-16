#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import nmf
import numpy as np

stocks = [
	'YHOO', 'AVP', 'BIIB', 'BP', 'CL', 'CVX', 'BIDU',
	'XOM', 'EXPE', 'GOOG', 'INTC', 'PG', 'MSFT'
]

def read(filename):
	f = open(filename)
	reader = csv.reader(f)
	reader.next();

	result = []
	for line in reader:
		result.append(line)
	return result

def get_stock(stock):
	data = open('csv/' + stock)
	reader = csv.reader(data)
	reader.next()

	result = []
	for line in reader:
		result.append(line)
	return result

def get_volumn():
	shortest = 300
	volumn = []
	dates = None
	for stock in stocks:
		data = get_stock(stock)
		if(len(data) < shortest):
			shortest = len(data)	
		volumn.append([float(d[5]) for d in data])
		
		if not dates:
			dates = [d[0] for d in data]

	for i in range(len(volumn)):
		volumn[i] = volumn[i][0:shortest]

	return volumn, dates[0: shortest]

def get_feature():
	v, dates = get_volumn()
	w, h = nmf.factorize(np.matrix(v).transpose(), pc=5)
	
	print w.shape, h.shape
	for i in range(np.shape(h)[0]):
		print "Feature %d" %i

		# get stock according to current feature
		ol = [(h[i,j], stocks[j]) for j in range(np.shape(h)[1])]
		ol.sort()
		ol.reverse()
		for j in range(np.shape(h)[1]):
			print ol[j]
		print

		# get the date
		porder = [(w[d, i], d) for d in range(len(dates))]
		porder.sort()
		porder.reverse()
		print [(p[0], dates[p[1]]) for p in porder[0:5]]
		print

if  __name__ == '__main__':
	get_feature()
