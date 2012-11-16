# -*- coding: UTF-8 -*-

import sqlite3
from math import tanh

class neural:
    def __init__(self, db="neural.db"):
        self.con = sqlite3.connect(db)
    
    def __del__(self):
        self.con.close()

    def createtables(self):
        self.con.execute("create table hiddennode(create_key)")
        self.con.execute("create table wordhidden(fromid, toid, strength)")
        self.con.execute("create table hiddenurl(fromid, toid, strength)")
        self.con.commit()

    def getstrength(self, fromid, toid, layer):
        if layer == 0: table = "wordhidden"
        else: table = "hiddenurl"

        res = self.con.execute(
            "select strength from %s where fromid=%d and toid=%d" %
            (table, fromid, toid)
        ).fetchone()

        if res == None:
            if layer == 0: return -0.2
            elif layer == 1: return 0

        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0: table = "wordhidden"
        else: table = "hiddenurl"

        res = self.con.execute(
            "select rowid from %s where fromid=%d and toid=%d" %
            (table, fromid, toid)
        ).fetchone()

        if res == None:
            self.con.execute(
                'insert into %s(fromid,toid,strength) values (%d,%d,%f)' %
                (table, fromid, toid, strength)
            )
        else:
            rowid = res[0]
            self.con.execute(
                'update %s set strength=%f where rowid=%d' %
                (table, strength, rowid)
            )

    def genhiddennode(self, wordids, urls):
        if len(wordids) == 0: return None
        key = '_'.join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute(
            "select rowid from hiddennode where create_key='%s'" % key
        ).fetchone()

        if res == None:
            cur = self.con.execute(
                "insert into hiddennode(create_key)values('%s')" % key
            )
            hiddenid = cur.lastrowid
            # set default strength
            for wi in wordids:
                self.setstrength(wi, hiddenid, 0, 1.0/len(wordids))

            for ui in urls:
                self.setstrength(hiddenid, ui, 1, 0.1)
            self.con.commit()

    def getallhiddenids(self, wordids, urlids):
        ll = {}
        for wi in wordids:
            cur = self.con.execute(
                'select toid from wordhidden where fromid=%d' % wi
            )
            for row in cur: ll[row[0]] = 1

        for ui in urlids:
            cur = self.con.execute(
                'select fromid from hiddenurl where toid=%d' %ui
            )
            for row in cur: ll[row[0]] = 1
        return ll.keys()

    def setupnetwork(self, wordids, urlids):
        # values
        self.wordids = wordids
        self.hiddenids = self.getallhiddenids(wordids, urlids)
        self.urlids = urlids

        # output of node
        self.ai = [1.0] * len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)

        # set up weight matrix
        self.wi = [[self.getstrength(wordid, hiddenid, 0)
                    for hiddenid in self.hiddenids]
                    for wordid in self.wordids]

        self.wo = [[self.getstrength(hiddenid, urlid, 1)
                    for urlid in self.urlids]
                    for hidden in self.hiddenids]

    def feedforward(self):
        # input layer
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # hidden layer
        for i in range(len(self.hiddenids)):
            sum = 0.0
            for j in range(len(self.wordids)):
                sum = sum + self.ai[j] * self.wi[j][i]
            self.ah[i] = tanh(sum)

        # output layer
        for i in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][i]
            self.ao[i] = tanh(sum)
        
        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward()
