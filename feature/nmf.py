# -*- coding: UTF-8 -*-

import numpy as np
import random

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
		if i % 10 == 0: print i, cost
		if cost == 0: break

		# update feature matrix
		hn = (np.transpose(w) * v)
		hd = (np.transpose(w) * w * h)
		h = np.matrix(np.array(h) * np.array(hn) / np.array(hd))

		# update weight matrix
		wn = (v * np.transpose(h))
		wd = (w * h * np.transpose(h))
		w = np.matrix(np.array(w) * np.array(wn) / np.array(wd))

	return w, h

