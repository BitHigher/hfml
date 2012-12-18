#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import matplotlib.pyplot as plt

def read_stock(filename):
	f = open(filename)
	reader = csv.reader(f)
	reader.next()

	d = []
	o = []
	c = []
	v = []
	for line in reader:
		d.append(line[0])
		o.append(float(line[1]))
		c.append(float(line[4]))
		v.append(float(line[5]))

	d.reverse()
	o.reverse()
	c.reverse()
	v.reverse()
	return d, o, c, v

def draw(filename):
	d, o, c, v = read_stock(filename)
	x = [i for i in range(len(d))]

	def get_date(x, pos):
		if(int(x) < len(d) and int(x) >= 0):
			return d[int(x)]
		return ""

	plt.figure(figsize=(20, 10))
	
	plt.subplot(211)
	formatter = plt.FuncFormatter(get_date)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.grid(True)
	plt.plot(x, o, 'r', label="Open")
	plt.plot(x, c, 'g', label="Close")
	plt.legend()

	plt.subplot(212)
	formatter = plt.FuncFormatter(get_date)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.grid(True)
	plt.plot(x, v, label="Volumn")
	plt.legend()

	plt.savefig('images/' + filename + '.png')


if __name__ == '__main__':
	import sys
	if(len(sys.argv) < 2):
		print 'Usage: stock_draw.py stock_data'
		sys.exit(-1)

	draw(sys.argv[1])

	
