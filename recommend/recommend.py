#!/usr/bin/python
import sys
sys.path.append('..')
import modules.similarity as sim

def genUserBasedMap(file = 'u.data'):
    map = {}
    f = open(file)
    for line in f:
        (user, item, rate) = line.split('\t')[0:3]
        map.setdefault(int(user), {})
        map[int(user)][int(item)] = int(rate)
    f.close()
    return map

def genItemBasedMap(file = 'u.data'):
    map = {}
    f = open(file)
    for line in f:
        (user, item, rate) = line.split('\t')[0:3]
        map.setdefault(int(item), {})
        map[int(item)][int(user)] = int(rate)
    f.close()
    return map

def userBased(map, person, n=5, similarity=sim.pearson):
    items = {}
    itemsSim = {}
    for p in map:
        if(p == person): continue
        score = distance(map, p, person, similarity)
        if(score <= 0): continue
        for i in map[p]:
            if(i != 0 and i != None and i not in map[person]):
                items.setdefault(i, 0)
                itemsSim.setdefault(i, 0)
                items[i] += score * map[p][i]
                itemsSim[i] += score
    
    #normalize the items 
    rankings = [(total/itemsSim[item], item) for item, total in items.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]
    
def itemBased(map, item, n = 5, similarity=sim.pearson):
    score = []
    for i in map:
        if i == item: continue
        score.append((distance(map, item, i, similarity), i))
        
    score.sort()
    score.reverse()
    return score[0:n]
    
def distance(map, p1, p2, similarity):
    si = {}
    for item in map[p1]:
        if item in map[p2]:
            si[item] = 1
    if len(si) == 0: return 0
    
    # calc the distance
    v1 = [map[p1][i] for i in si]
    v2 = [map[p2][i] for i in si]
    distance = similarity(v1, v2)
    return distance
