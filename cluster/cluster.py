#!/usr/bin/python
import sys
sys.path.append('..')
import modules.similarity as sim
import random

words = []
blogs = []
data = []

def getData(file = 'blogdata.txt'):
    global words, map
    f = open(file)
    line = f.readline()
    words = line.strip().split('\t')[1:]
    
    for line in f:
        p = line.strip().split('\t')
        blogs.append(p[0])
        data.append([float(x) for x in p[1:]])
    f.close()
    
def hcluster(similarity = sim.pearson):
    global data
    clusters = [bicluster(data[i], id=i) for i in range(len(data))]
    
    currentId = -1 # id for merged bicluster
    dis = {}    #record the distance computed before
    while(len(clusters) > 1):
        closestIndex = (0, 1)
        closestKey = (clusters[0].id, clusters[1].id)
        if closestKey not in dis:
            dis[closestKey] = 1 - similarity(clusters[0].vec, clusters[1].vec)
        closest = dis[closestKey]
        
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                key = (clusters[i].id, clusters[j].id)
                if key not in dis:
                    dis[key] = 1 - similarity(clusters[i].vec, clusters[j].vec)
                if(dis[key] < closest):
                    closest = dis[key]
                    closestKey = key
                    closestIndex = (i, j)
        
        # generate a new bicluster and delete the closePair
        mergedVec = [(clusters[closestIndex[0]].vec[i] + clusters[closestIndex[1]].vec[i])/2.0 
            for i in range(len(clusters[0].vec))]
        clusters.append(bicluster(mergedVec, 
                                   clusters[closestIndex[0]], 
                                   clusters[closestIndex[1]], 
                                   closest, 
                                   currentId))
        currentId -= 1
        del dis[closestKey]
        
        #ATTENTION!!! remove the later one first
        #ATTENTION!!! because the index will change if remove the former one first
        del clusters[closestIndex[1]]   
        del clusters[closestIndex[0]]
        print closestIndex, closestKey
        
    return clusters[0]
        
def rotateData():
    global data
    newData = []
    for i in range(len(data[0])):
        newData.append([data[j][i] for j in range(len(data))])
    
    data = newData
        
def printCluster(cluster, labels, n=0):
    if cluster == None: return
    for i in range(n):
        print ' ',
    if(cluster.id >= 0):
        print '-',  labels[cluster.id]
    else:
        print '+', cluster.id
        printCluster(cluster.left, labels, n+1)
        printCluster(cluster.right, labels, n+1)
    
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id
        
        
def kmeans(k=5, iterations=100, similarity=sim.pearson):
    global data
    if(len(data) <= k): return data
    
    clusters = [[] for i in range(k)]
    length = len(data[0])
    ranges = [(min(row[i] for row in data), max(row[i] for row in data)) 
                for i in range(length)]
    #random k centers
    centers = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
                for i in range(length)]
                for j in range(k)]
    
    # in case of falling into endless loop
    while(iterations > 0):
        iterations -= 1
        clusters = [[] for i in range(k)]
        newCenters = [[0 for i in range(length)] for j in range(k)]
        for i in range(len(data)):
            minVal = 1 - similarity(data[i], centers[0])
            minIndex = 0
            for j in range(1, k):
                curMin = 1 - similarity(data[i], centers[j])
                if curMin < minVal:
                    minVal = curMin
                    minIndex = j
                    
            clusters[minIndex].append(i)
            newCenters[minIndex] = [newCenters[minIndex][j] + data[i][j] for j in range(length)]
            
        for i in range(k):
            num = float(len(clusters[i]))
            if(num > 0):
                newCenters[i] = [newCenters[i][j] / num for j in range(length)]
        
        if(newCenters == centers):
            return clusters
        else:
            centers = newCenters

    return clusters
