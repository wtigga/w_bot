# -*- encoding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3 as sqlite
import re

ignorewords = set(['the', 'if', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:

    # init crawler with dbname
    def __init__(self, dbname):
        print('open connect')
        self.con = sqlite.connect(dbname)


    def __del__(self):
        print('close connect')
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    # get id and ad entry if not present
    def getentryid(self, table, field, value, createnew=True):
        cur = self.con.execute(
            "select rowid from %s where %s = '%s'" % (table, field, value)
        )
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
                'insert into %s (%s) values ("%s")' % (table, field, value)
            )
            return cur.lastrowid
        else:
            return res[0]

    # indexing of one page
    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        print('Indexing %s' % url)

        # get words list
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # get url id
        urlid = self.getentryid('urllist', 'url', url)

        # link every word with url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid, wordid, location) values (%d, %d, %d)' % (urlid, wordid, i))

    # getting only text from html
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # tokenizing text
    def separatewords(self, text):
        splitter = re.compile('\\W+')
        return [s.lower() for s in splitter.split(text) if s != '']

    # return True if URL is indexed
    def isindexed(self, url):
        u = self.con.execute(
            "select rowid from urllist where url = '%s'" % url
        ).fetchone()
        if u != None:
            # check if page is visited
            v = self.con.execute(
                'select * from wordlocation where urlid = %d' % u[0]
            ).fetchone()
            if v != None: return True
        return False

    # adding link from one page to another
    def addlinkref(self, urlFrom, urlTo, linkText):
        words = self.separatewords(linkText)
        fromid = self.getentryid('urllist', 'url', urlFrom)
        toid = self.getentryid('urllist', 'url', urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid, toid) values (%d,%d)" % (fromid, toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into linkwords(linkid, wordid) values (%d,%d)" % (linkid, wordid))

    # crawling to depth
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = requests.get(page)
                except:
                    print('cannot open %s' % page)
                    continue
                soup = BeautifulSoup(c.text)
                self.addtoindex(page, soup)

                links = soup.findAll('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1: continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                    self.dbcommit()
            pages = newpages

    # creating tables in db
    def createindextables(self):
        # self.con.execute('drop table link')
        # self.con.execute('drop table linkwords')
        # self.con.execute('drop table urllist')
        # self.con.execute('drop table wordlist')
        # self.con.execute('drop table wordlocation')
        exec_drop_list = ['drop table link',
                          'drop table linkwords',
                          'drop table urllist',
                          'drop table wordlist',
                          'drop table wordlocation']
        exec_list = ['create table link(fromid integer, toid integer)',
                    'create table linkwords(wordid, linkid)',
                    'create table urllist(url)',
                    'create table wordlist(word)',
                    'create table wordlocation(urlid, wordid, location)',
                    'create index urltoidx on link(toid)',
                    'create index urlfromidx on link(fromid)',
                    'create index urlidx on urllist(url)',
                    'create index wordidx on wordlist(word)',
                    'create index wordurlidx on wordlocation(wordid)'
                     ]
        for command in exec_list:
            try:
                self.con.execute(command)
            except sqlite.OperationalError:
                continue
        self.dbcommit()
        print('table set finished')

url = 'https://bkrs.info/taolun/index.php'
crawler = crawler('searchindex.db')
crawler.createindextables()
# crawler.crawl([url])
