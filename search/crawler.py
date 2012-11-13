# -*- coding: UTF-8 -*-
import sqlite3
import urllib2
from bs4 import BeautifulSoup as bs
from urlparse import urljoin

import sys
sys.path.append('..')
import modules.fenci as fenci
fenci.init()

class crawler:
    def __init__(self, db="search.sqlite"):
        self.con = sqlite3.connect(db)
    
    def __del__(self):
        self.con.close()


    def createtables(self):
        #create tables
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        
        #create indices
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index fromidx on link(fromid)')
        self.con.execute('create index toidx on link(toid)')
        self.con.commit()
    
    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
        return u != None
   
    def getentryid(self, table, field, value, createnew = True):
        cur = self.con.execute(
            "select rowid from %s where %s='%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
                "insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    def addpage(self, url, content):
        words = {}
        try:
            words= fenci.solve(content, fenci.mmseg)
        except:
            return

        urlid = self.getentryid('urllist', 'url', url)
        for word in words:
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute(
                "insert into wordlocation(urlid, wordid, location) values(%d, %d, %d)" % (urlid, wordid, words[word]))

        self.con.commit()
    
    def addlink(self, fromurl, tourl, content):
        words = {}
        try:
            words= fenci.solve(content, fenci.mmseg)
        except:
            words = {}

        fromid = self.getentryid('urllist', 'url', fromurl)
        toid = self.getentryid('urllist', 'url', tourl)
        cur = self.con.execute(
            "insert into link(fromid, toid) values(%d, %d)" % (fromid, toid))

        linkid = cur.lastrowid
        for word in words:
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute(
                "insert into linkwords(wordid, linkid) values(%d, %d)" % (wordid, linkid))

        self.con.commit()
            


    #crawl the url and put links in that page into urlset
    def crawlpage(self, url, urlset):
        c = None
        try:
            c = urllib2.urlopen(url)
        except: 
            return
            
        content = c.read()
        if (content == None or len(content)==0): return
        self.addpage(url, content)
        
        soup = None
        try:
            soup = bs(content)
        except:
            return

        links = soup("a")
        for link in links:
            if('href' in dict(link.attrs)):
                newurl = urljoin(url, link['href'])
                urlset.add(newurl)
                #TODO the url may contain illegal characters
                try:
                    self.addlink(url, newurl, link.string)
                except:
                    pass
        
    
    def crawl(self, startList, depth=None):
        urls = set(startList)
        curDepth = 0
        while(depth == None or (curDepth < depth)):
            print "URLS: ", len(urls)
            curDepth += 1
            newUrls = set()
            for url in urls:
                self.crawlpage(url, newUrls) 
            urls = newUrls
