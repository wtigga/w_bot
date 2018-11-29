# -*- encoding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3 as sqlite
import re
from time import time

ignorewords = set(['the', 'if', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:

	# init crawler with dbname
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

	# get id and add entry if not present
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

	# indexing one page
	def addtoindex(self, url, soup):
		if self.isindexed(url): return
		# print('Added to index %s' % url

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

	# return True if URL is indexed else False
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
	def crawl(self, page):

		newpages = set()
		try:
			c = requests.get(page)
			print('soup for crawling %s' % page)
		except:
			print('cannot open %s' % page)
			return

		soup = BeautifulSoup(c.text, features="html.parser")

		self.addtoindex(page, soup)

		links = soup.findAll('a')
		print('got %s links from crawled url from %a' % (len(links), page))
		q = (page, "", "Y")
		try:
			self.con.execute('insert into urlcheck values (?, ?, ?)', q)
			print("put %s into urlcheck" % page)
		except sqlite.IntegrityError:
			isindexed = self.con.execute('select indexed from urlcheck where url = "%s"' % page).fetchone()
			if isindexed[0] == 'Y':
				print('%s is already crawled' % page)
				return
			else:
				self.con.execute('update urlcheck set indexed = "Y" where url = "%s"' % page)
				print("change %s n to y" % page)

		for link in links:
			if 'href' in dict(link.attrs):
				url = urljoin(page, link['href'])
				if url.find("'") != -1: continue
				url = url.split('#')[0]
				# if url[0:4] == 'http' and 'bkrs.info' in url and not self.isindexed(url):
				isindexed = self.con.execute('select indexed from urlcheck where url = "%s"' % url).fetchone()
				if url[0:4] == 'http' and 'bkrs.info' in url and 'taolun' in url and not isindexed:
					if 'slovo' not in url:
						newpages.add(url)
						q = (url, link.string, "N")
						self.con.execute('insert into urlcheck values (?, ?, ?)', q)
				linkText = self.gettextonly(link)
				self.addlinkref(page, url, linkText)

				# topicId = re.search(url, '.*taolun\/(forum|thread)-(\d+)(-.*)*\.html')
			self.dbcommit()
		print('commit links from one url')
		self.dbcommit()
		print('commit set of urls')
		print('added %s links for newpages from %a' % (len(newpages), page))


	def crawl_init(self, page):
		print('getting initial page')
		newpages = set()
		c = requests.get(page)
		soup = BeautifulSoup(c.text, features="html.parser")

		links = soup.findAll('a')
		for link in links:
			if 'href' in dict(link.attrs):
				url = urljoin(page, link['href'])
				newpages.add(url)

		return newpages


	# creating tables in db
	def createindextables(self, reset=False):

		exec_drop_list = ['drop table if exists link',
		                  'drop table if exists linkwords',
		                  'drop table if exists urllist',
		                  'drop table if exists wordlist',
		                  'drop table if exists wordlocation',
		                  'drop table if exists urlcheck']

		exec_list_reset = ['create table link(fromid integer, toid integer)',
		                   'create table linkwords(wordid, linkid)',
		                   'create table urllist(url)',
		                   'create table wordlist(word)',
		                   'create table wordlocation(urlid, wordid, location)',
		                   'create index urltoidx on link(toid)',
		                   'create index urlfromidx on link(fromid)',
		                   'create index urlidx on urllist(url)',
		                   'create index wordidx on wordlist(word)',
		                   'create index wordurlidx on wordlocation(wordid)',
		                   'create table urlcheck(url unique, text, indexed)']

		if reset == True:
			for command in exec_drop_list:
				try:
					self.con.execute(command)
				except sqlite.OperationalError:
					continue
		for command in exec_list_reset:
			try:
				self.con.execute(command)
			except sqlite.OperationalError:
				continue

		exec_list = ['create table if not exists link(fromid integer, toid integer)',
		             'create table if not exists linkwords(wordid, linkid)',
		             'create table if not exists urllist(url)',
		             'create table if not exists wordlist(word)',
		             'create table if not exists wordlocation(urlid, wordid, location)',
		             'create index if not exists urltoidx on link(toid)',
		             'create index if not exists urlfromidx on link(fromid)',
		             'create index if not exists urlidx on urllist(url)',
		             'create index if not exists wordidx on wordlist(word)',
		             'create index if not exists wordurlidx on wordlocation(wordid)',
		             'create table if not exists urlcheck(url unique, text, indexed)']

		for command in exec_list:
			try:
				self.con.execute(command)
			except sqlite.OperationalError:
				continue
		self.dbcommit()
		print('table set finished')


crawler = crawler('searchindex.db')

def run(pages):
	crawler.crawl(pages[0])
	sqlq = 'select url from urlcheck where indexed = "N" order by random() limit 1'
	pages = [i[0] for i in crawler.con.execute(sqlq).fetchall()]
	if len(pages) > 0:
		run(pages)


sqlq = 'select url from urlcheck where indexed = "N" order by random() limit 1'
pages = [i[0] for i in crawler.con.execute(sqlq).fetchall()]
if len(pages) > 0:
	run(pages)