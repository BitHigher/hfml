# -*- coding: UTF-8 -*-

import similarity as sim
from random import random
from math import sqrt

def multiscale(data, similarity=sim.pearson, rate=0.01):
	n = len(data)

	# the real distances between every pair of items
	realdist = [[1-similarity(data[i], data[j]) for j in range(n)]
				for i in range(n)]

	outersum = 0.0
	
	# randomly initialize the starting point of each data in 2D
	loc = [[random(), random()] for i in range(n)]
	fakedist = [[0.0 for j in range(n)] for i in range(n)]

	lasterror = None
	for m in range(0, 1000):
		# calc distance
		for i in range(n):
			for j in range(n):
				fakedist[i][j] = sqrt(sum([pow(loc[i][k]-loc[j][k], 2)
											for k in range(len(loc[i]))]))

		# move points
		grad = [[0.0, 0.0] for i in range(n)]

		totalerror = 0
		for i in range(n):
			for j in range(n):
				if j == k: continue
				# in case of dividing by zero
				errorterm = (fakedist[i][j]-realdist[i][j])/(realdist[i][j] + 0.01)

				grad[i][0] += (loc[i][0]-loc[j][0])/(fakedist[i][j]+0.01) * errorterm	
				grad[i][1] += (loc[i][1]-loc[j][1])/(fakedist[i][j]+0.01) * errorterm

				totalerror += abs(errorterm)
		print totalerror

		# if answer got worse, stop
		if lasterror and lasterror < totalerror: break
		lasterror = totalerror

		# move each point
		for i in range(n):
			loc[i][0] -= rate*grad[i][0]
			loc[i][1] -= rate*grad[i][1]

	return loc
