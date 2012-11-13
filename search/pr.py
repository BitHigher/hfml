# -*- coding: UTF-8 -*-
import sqlite3

class pagerank:
    def __init__(self, db="search.sqlite"):
        self.con = sqlite3.connect(db)
        self.damping = 0.85

    def __del__(self):
        self.con.close()

    def calconce(self):
        # calclate the newpr of each page
        self.con.execute(
            "update urllist set newpr=( \
                select %f+sum(u.pr/u.outer*%f) \
                from urllist u, link l \
                where u.rowid=l.fromid and urllist.rowid=l.toid \
                group by l.toid \
            )" % (1-self.damping, self.damping)
        )
        self.con.commit()

        # set the pr to new newpr of each page
        self.con.execute(
            "update urllist set pr=newpr"
        )
        self.con.commit()

    def calc(self, iterations=20):
        # calculate the number of outer links of each page
        self.con.execute(
            "update urllist set outer = ( \
                select count(l.toid) \
                from link l \
                where urllist.rowid=l.fromid \
                group by l.fromid)"
        )
        self.con.commit()        

        for i in range(iterations):
            print 'Iteration ', i+1, '...'
            self.calconce()
