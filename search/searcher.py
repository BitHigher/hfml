# -*- coding: UTF-8 -*-
import sqlite3

import sys
sys.path.append('..')
import modules.fenci as fenci
fenci.init()

class searcher:
    def __init__(self, db="search.sqlite"):
        self.con = sqlite3.connect(db)

    def __del__(self):
        self.con.close()

    def geturl(self, urlid):
        cur = self.con.execute(
            "select url from urllist where rowid=%d" % urlid
        ).fetchone()

        if cur != None:
            return cur[0]
        else:
            return None


    def query(self, qstring):
        words = fenci.solve(qstring)
        if len(words) == 0: return
        
        #get word ids
        wordids = []
        tables = 0
        tablelist = ''
        clauselist = ''
        fieldlist = 'w0.urlid'
        for word in words:
            row = self.con.execute(
                "select rowid from wordlist where word='%s'" % word
            ).fetchone()
            
            if row != None:
                wordid = row[0]
                wordids.append(wordid)
                if tables > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tables-1, tables)
                fieldlist += ',w%d.location' % tables
                tablelist += 'wordlocation w%d' % tables
                clauselist += 'w%d.wordid=%d' % (tables, wordid)
                tables += 1

        # full sql
        fullsql = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        print 'SQL: ', fullsql
        cur = self.con.execute(fullsql)
        rows = [row for row in cur]
        return rows, wordids

    def frequency(self, rows, worids):
        weight = {}
        for row in rows:
            weight[row[0]] = 0
            for i in range(1, len(row)):
                weight[row[0]] += row[i]

        weight = sorted(weight.items(), key=lambda x:x[1], reverse=True)
        return weight

    def geturls(self, weight):
        urls = [(item[1], self.geturl(item[0])) for item in weight]
        return urls
