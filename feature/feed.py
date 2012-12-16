#!/usr/bin/python
# -*- coding: UTF-8 -*-
import feedparser as fp
import numpy as np
import random

import sys
sys.path.append('..')
import modules.fenci as fenci
fenci.init()

feedlist = [
	'http://rss.news.sohu.com/rss/guonei.xml',
	'http://rss.news.sohu.com/rss/guoji.xml',
	'http://rss.news.sohu.com/rss/shehui.xml',
	'http://rss.news.sohu.com/rss/junshi.xml',
	'http://rss.news.sohu.com/rss/sports.xml',
	'http://rss.news.sohu.com/rss/it.xml',
	'http://rss.news.sohu.com/rss/business.xml',
	'http://rss.news.sohu.com/rss/yule.xml',
	'http://rss.news.sohu.com/rss/learning.xml'
];

def getwords():
	allwords = {}
	articlewords = []
	articletitles = []
	ec = 0
	for feed in feedlist:
		f = fp.parse(feed)
		for e in f.entries:
			if e.title in articletitles: continue

			#get words
			words = fenci.solve(e.title.encode('utf8') + e.description.encode('utf8'),
								fenci.mmseg)
			articletitles.append(e.title)
			articlewords.append({})

			for w in words:
				allwords.setdefault(w, 0)
				allwords[w] += 1
				articlewords[ec].setdefault(w, 0)
				articlewords[ec][w] += 1
			ec += 1
	return allwords, articlewords, articletitles

def makematrix(allw, articlew):
	wordvec = []
	for w, c in allw.items():
		# only get the normal words
		if c > 3 and c < len(articlew)*0.6:
			wordvec.append(w)

	# make matrix
	matrix = [[((word in f and f[word]) or 0) for word in wordvec] for f in articlew]
	return matrix, wordvec

def diffcost(m1, m2):
	diff = 0
	for i in range(np.shape(m1)[0]):
		for j in range(np.shape(m1)[1]):
			diff += (m1[i,j]-m2[i,j])**2
	return diff

def factorize(v, pc=10, iteration=50):
	ic = np.shape(v)[0]
	fc = np.shape(v)[1]

	# create weight matrix and feature matrix randomly
	w = np.matrix([[random.random() for j in range(pc)] for i in range(ic)])	
	h = np.matrix([[random.random() for j in range(fc)] for i in range(pc)])

	for i in range(iteration):
		wh = w * h
		cost = diffcost(v, wh)
		if i % 10 == 0: print cost

		if cost == 0: break

		# update feature matrix
		hn = (np.transpose(w) * v)
		hd = (np.transpose(w) * w * h)
		try:
			h = np.matrix(np.array(h) * np.array(hn) / np.array(hd))
		except:
			pass

		# update weigth matrix
		wn = (v * np.transpose(h))
		wd = (w * h * np.transpose(h))
		try:
			print np.array(wd)
			w =	np.matrix(np.array(w) * np.array(wn) / np.array(wd))
		except:
			pass

	return w, h


def test():
	allw, aw, at = getwords()
	m, v = makematrix(allw, aw)
	weigth, feat = factorize(np.matrix(m), pc=20, iteration=50)

	return weight, feat

#test()
