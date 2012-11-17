# -*- coding: UTF-8 -*-
import time
import sys
import random
import math

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60 + x[4]

def m2t(minutes):
    return '%02d:%02d' % (minutes/60, minutes%60)

people = [('Seymour', 'BOS'),
            ('Franny', 'DAL'),
            ('Zooey', 'CAK'),
            ('Walt', 'MIA'),
            ('Buddy', 'ORD'),
            ('Les', 'OMA')]

destination = 'LGA'
flights = {}
# read flights from file
for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest),[])

    flights[(origin, dest)].append(
        (getminutes(depart), 
        getminutes(arrive), 
        int(price)))

def output(r):
    for d in range(len(r)/2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d+1]]

        print ('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' %
                (name, origin, 
                m2t(out[0]), m2t(out[1]), out[2],
                m2t(ret[0]), m2t(ret[1]), ret[2]))

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60
    totalwait = 0

    for d in range(len(sol)/2):
        origin = people[d][1]
        out = flights[(origin, destination)][sol[2*d]]
        ret = flights[(origin, destination)][sol[2*d+1]]

        totalprice += out[2] + ret[2]

        if latestarrival < out[1]: latestarrival = out[1]
        if earliestdep > ret[0]: earliestdep = ret[0]
    
    for d in range(len(sol)/2):
        origin = people[d][1]
        out = flights[(origin, destination)][sol[2*d]]
        ret = flights[(origin, destination)][sol[2*d+1]]

        totalwait += (latestarrival-out[1]) + (ret[0]-earliestdep)

    if latestarrival > earliestdep: totalprice += 50
    return totalprice + totalwait

def randomopt(domain, costf):
  best = sys.maxint
  bestr = None
  for i in range(1000):
    r = [random.randint(domain[i][0], domain[i][1])
            for i in range(len(domain))]
    cost = costf(r)

    if cost < best:
        best = cost
        bestr = r
    return r

def hillclimb(domain, costf):
    sol = [random.randint(domain[i][0], domain[i][1])
            for i in range(len(domain))]

    while True:
        neighbours = []
        for j in range(len(domain)):
            if sol[j] > domain[j][0]:
                neighbours.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbours.append(sol[0:j] + [sol[j]+1] + sol[j+1:])

        #get best solution from neighbours
        current = costf(sol)
        best = current
        for j in range(len(neighbours)):
            cost = costf(neighbours[j])
            if cost < best:
                best = cost
                sol = neighbours[j]

        if best == current:
            break

    return sol
    
def annealing(domain, costf, T=10000.0, cool=0.95, step=1):
    sol = [random.randint(domain[i][0], domain[i][1])
                    for i in range(len(domain))]

    best = costf(sol)
    while T>0.1:
        #seelct a index
        i = random.randint(0, len(domain)-1)
        #select a direction
        direction = 0
        if random.random() < 0.5: direction = -step
        else: direction = step
        
        #create a new solution
        newsol = sol[:]
        newsol[i] += direction
        if newsol[i] < domain[i][0]: newsol[i] = domain[i][0]
        if newsol[i] > domain[i][1]: newsol[i] = domain[i][1]
    
        cost = costf(newsol)
        if (cost < best or random.random() < pow(math.e, -(cost-best)/T)):
            best = cost
            sol = newsol

        T *= cool
    return sol

def genetic(domain, costf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100):
    def mutate(sol):
        i = random.randint(0, len(domain)-1)
        if random.rand() < 0.5 and sol[i]-step >= domain[i][0]:
            return sol[0:i] + [sol[i]-step] + sol[i+1:]
        elif sol[i]+step <= domain[i][1]:
            return sol[0:i] + [sol[i]+step] + sol[i+1:]
            
    def crossover(sol1, sol2):
        i = random.randint(0, len(domain)-1)
        return sol1[0:i] + sol2[i:]

    #generate population
    pop = []
    for i in range(popsize):
        sol = [random.randint(domain[i][0], domain[i][1]) 
                for i in range(len(domain))]
        pop.append(sol)

    topelite = int(elite * popsize)

    best = pop[0]
    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()

        #in case there are some better solutions
        #so ensure that it will genetic 10 iterations
        if(i > 10 and best == scores[0][1]):
            break
        best = scores[0][1]

        ranked = [v for (s, v) in scores]
        #start from elite
        pop = ranked[0:topelite]

        #add mutation and crossover
        while len(pop) < popsize:
            if random.random < mutprob:
                c = random.randint(0, topelite-1)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, topelite-1)
                c2 = random.randint(0, topelite-1)
                pop.append(crossover(ranked[c1], ranked[c2]))

    scores = [(costf(v), v) for v in pop]
    scores.sort()
    return scores[0][1]
