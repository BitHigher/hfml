# -*- coding: UTF-8 -*-
import math
import sys
sys.path.append('..')
import modules.fenci as fenci

fenci.init()

def segment(doc):
    result = fenci.solve(doc)
    return result.keys()

class classifier:
    def __init__(self, getfeatures, filename=None):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures

    def incf(self, f, cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1


    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    def catcount(self, cat):
        if cat in self.cc:
            return self.cc[cat]
        return 0

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0: return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        basicprob = prf(f, cat)
        totals = sum([self.fcount(f,c) for c in self.categories()])

        bp = ((weight*ap)+(totals*basicprob)) / (weight+totals)
        return bp

class naivebayes(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.thresholds = {}
    
    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def docprob(self, item, cat):
        features = self.getfeatures(item)
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p

    # only returns the numerator of bayes equation
    def prob(self, item, cat):
        catprob = self.catcount(cat) / float(self.totalcount()) 
        docprob = self.docprob(item, cat)
        return docprob*catprob

    def classify(self, item, default=None):
        probs = {}

        maxprob = 0.0
        best = default
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if maxprob < probs[cat]:
                maxprob = probs[cat]
                best = cat

        if best == default: return best

        t = self.thresholds[best]
        for cat in probs:
            if cat == best: continue
            if best < t*probs[cat]: return default
        return best

class fisher(classifier):
    def cprob(self, f, cat):
        clf = self.fprob(f, cat)
        if clf == 0.0: return clf

        total = sum([self.fprob(f, c) for c in self.categories()])
        return clf / total

    def prob(self, item, cat):
        features = self.getfeatures(item)
        p = 1.0
        for f in features:
            p *= self.weightedprob(f, cat, self.cprob)
        fscore = -2*math.log(p)

        #TODO I can not understand the inverse chi-square distribution
        return fscore

