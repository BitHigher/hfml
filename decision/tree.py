# -*- coding: UTF-8 -*-

data = [line.split('\t') for line in file('data.txt')]
# remove the \n
for i in range(len(data)-1):
    data[i][4] = data[i][4][:-1]

# convert 3th for string to int
for i in range(len(data)):
    data[i][3] = int(data[i][3])

from math import log

class treenode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

def divideset(rows, column, value):
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column] == value

    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)

def uniquecounts(rows):
    results = {}
    for row in rows:
        r = row[len(row)-1]
        results.setdefault(r, 0)
        results[r] += 1

    return results

def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for f in counts:
        imp += pow(float(counts[f])/total, 2)
    return 1 - imp

def entropy(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    ent = 0.0
    for f in counts:
        p = float(counts[f]) / total
        ent -= p * log(p, 2)
    return ent

def buildtree(rows, scoref=entropy):
    if len(rows) == 0: return treenode()
    current_score = scoref(rows)

    best_gain = 0.0
    best_criteria = None
    best_sets = None
    
    column_count = len(rows[0]) - 1
    for col in range(column_count):
        column_values = set()
        for row in rows:
            column_values.add(row[col])
        for value in column_values:
            (set1, set2) = divideset(rows, col, value)

            #calculate the information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p*scoref(set1) - (1-p)*scoref(set2)

            if gain > best_gain and len(set1)>0 and len(set2)>0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    #create sub node
    if best_gain > 0:
        trueb = buildtree(best_sets[0])
        falseb = buildtree(best_sets[1])

        return treenode(col=best_criteria[0],
                            value=best_criteria[1],
                            tb=trueb,
                            fb=falseb)
    else:
        return treenode(results=uniquecounts(rows))

def prune(tree, mingain):
    if tree.tb != None and tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb != None and tree.fb.results == None:
        prune(tree.fb, mingain)

    if tree.tb.results != None and tree.fb.results != None:
        tb, fb = [],[]
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c
    
        pt = float(len(tb)) / (len(tb) + len(fb))
        delta = entropy(tb+fb)-pt*entropy(tb)-(1-pt)*entropy(fb)

        if delta < mingain:
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts(tb+fb)

def getwidth(tree):
    # count from leaf
    if tree.tb == None and tree.fb == None: return 1
    return getwidth(tree.tb) + getwidth(tree.fb)

def getdepth(tree):
    if tree.tb == None and tree.fb == None: return 0
    return max(getdepth(tree.tb), getdepth(tree.fb)) + 1

def drawnode(draw, tree, x, y):
    if tree.results == None:
        w1 = getwidth(tree.fb) * 100
        w2 = getwidth(tree.tb) * 100

        left = x-(w1+w2)/2
        right = x+(w1+w2)/2

        # draw criterion
        draw.text((x-20, y-10), str(tree.col)+':'+str(tree.value), (0, 0, 0))

        # draw lines to branches
        draw.line((x, y, left+w1/2, y+100), fill=(255, 0, 0))
        draw.line((x, y, right-w2/2, y+100), fill=(255, 0, 0))

        # draw branch node
        drawnode(draw, tree.fb, left+w1/2, y+100)
        drawnode(draw, tree.tb, right-w2/2, y+100)
    else:
        txt = ' \n'.join(['%s:%d' %v for v in tree.results.items()])
        draw.text((x-20, y), txt, (0, 0, 0))


def drawtree(tree, jpeg='tree.jpg'):
    from PIL import Image, ImageDraw
    w = getwidth(tree) * 100
    h = getdepth(tree) * 100 + 120
    img = Image.new('RGB', (w,h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    drawnode(draw, tree, w/2, 20)
    img.save(jpeg, 'JPEG')

def classify(observation, tree):
    # traverse from the root to a particular leaf
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value: branch = tree.tb
            else: branch = tree.fb
        else:
            if v == tree.value: branch = tree.tb
            else: branch = tree.fb
        return classify(observation, branch)


def mdclassify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        # the value in position tree.col is missed
        if v == None:
            tr, fr = mdclassify(observation, tree.tb), mdclassify(observation, tree.fb)
            # treat all results {'Basic', 'None', 'Premium'} as the small
            tcount = sum(tr.values())
            fcount = sum(fr.values())
            tw = float(tcount) / (tcount+fcount)
            fw = 1.0 - tw
            result = {}
            for k, v in tr.items(): result[k] = v*tw
            for k, v in fr.items():
                if k not in result: result[k] = 0
                result[k] += v*fw
            return result
        else:
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value: branch = tree.tb
                else: branch = tree.fb
            else:
                if v == tree.value: branch = tree.tb
                else: branch = tree.fb
            return mdclassify(observation, branch)

