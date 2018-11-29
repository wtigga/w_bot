import sqlite3 as sqlite

class searcher:

	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def getmatchrows(self, q):
		fieldlist = 'w0.urlid'
		tablelist = ''
		clauselist = ''
		wordids = []

		words = q.split(' ')
		tablenumber = 0

		for word in words:
			wordrow = self.con.execute('select rowid from wordlist where word = "%s"' % word).fetchone()
			if wordrow != None:
				wordid = wordrow[0]
				wordids.append(wordid)
				if tablenumber > 0:
					tablelist += ', '
					clauselist += ' and '
					clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber-1, tablenumber)
				fieldlist += ', w%d.location' % tablenumber
				tablelist += 'wordlocation w%d' % tablenumber
				clauselist += 'w%d.wordid = %d' % (tablenumber, wordid)
				tablenumber += 1

		fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
		print(fullquery)
		try:
			cur = self.con.execute(fullquery)
		except sqlite.OperationalError:
			cur = []
		rows = [row for row in cur]
		# rows = [(1, 320), (1, 321),...
		# wordids = [194]
		return rows, wordids

	def normalizedscores(self, scores, smallIsBetter=0):
		vsmall = 0.00001
		if smallIsBetter:
			minscore = min(scores.values())
			return dict([(u, float(minscore)/max(vsmall, l)) for (u, l) in scores.items()])
		else:
			maxscore = max(scores.values())
			if maxscore == 0: maxscore = vsmall
			return dict([u, float(c)/maxscore] for (u,c) in scores.items())

	def frequencyscore(self, rows):
		counts = dict([(row[0], 0) for row in rows])
		for row in rows: counts[row[0]] += 1
		return self.normalizedscores(counts)

	def getscoredlist(self, rows, wordids):
		totalscores = dict([(row[0], 0) for row in rows])
		# totalscores = {1: 0, 30: 0,..

		weights = [(1.0, self.frequencyscore(rows))]
		# weights = [(1.0, {1: 0.5714285714285714, 30: 0.14285714285714285,..
		# weights = [(1.0, self.locationscore(rows))]
		weights = [
			(1.0, self.locationscore(rows))
			,(1.5, self.frequencyscore(rows))
			,(0.5, self.distancescore(rows))
			,(1.0, self.pagerankscore(rows))
			,(1.0, self.linktextscore(rows, wordids))
		]

		for (weight, scores) in weights:
			for url in totalscores:
				totalscores[url] += weight * scores[url]

		# totalscores = {1: 0.5714285714285714, 30: 0.14285714285714285,
		return totalscores

	def geturlname(self, id):
		return self.con.execute(
			'select url from urllist where rowid=%d' % id
		).fetchone()[0]

	def locationscore(self, rows):
		# rows = [(1, 320), (1, 321),..
		locations = dict([(row[0], 1000000) for row in rows])
		# locations = {1: 1000000, 30: 1000000,..
		for row in rows:
			loc = sum(row[1:])
			# row = (1, 320)
			# loc = 320
			if loc < locations[row[0]]: locations[row[0]] = loc
		# locations = {1: 320, 30: 403,..
		return self.normalizedscores(locations, smallIsBetter=1)

	def distancescore(self, rows):
		if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])
		mindistance = dict([(row[0], 1000000) for row in rows])
		for row in rows:
			dist = sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
			if dist < mindistance[row[0]]: mindistance[row[0]] = dist
		return self.normalizedscores(mindistance, smallIsBetter=1)

	def inboundlinkscore(self, rows):
		uniqueurls = set(row[0] for row in rows)
		inboundcount = dict([(u, self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])
		return self.normalizedscores(inboundcount)

	def pagerankscore(self, rows):
		pageranks = dict([(row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
		maxrank = max(pageranks.values())
		normalizedscores = dict([(u, float(1)/maxrank) for (u, l) in pageranks.items()])
		return normalizedscores

	def linktextscore(self, rows, wordids):
		linkscores = dict([(row[0], 0) for row in rows])
		for wordid in wordids:
			cur = self.con.execute(
				'select link.fromid, link.toid from linkwords, link where wordid = %d and linkwords.linkid = link.rowid' % wordid
			)
			for (fromid, toid) in cur:
				if toid in linkscores:
					pr = self.con.execute('select score from pagerank where urlid = %d' % fromid).fetchone()[0]
					linkscores[toid] += pr
		maxscore = max(linkscores.values())
		normalizedscores = dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
		return normalizedscores

	def query(self, q):
		rows, wordlists = self.getmatchrows(q)
		scores = self.getscoredlist(rows, wordlists)
		rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse = True)
		# rankedscores = [(1.0, 39), (1.0, 32),...
		for (score, urlid) in rankedscores[0:10]:
			print('%f\t%s' % (score, self.geturlname(urlid)))

s = searcher('searchindex.db')
q = s.query('деньги')
q
# for i in q[0]:
# 	print(i)
# 	url = i[0]
# 	s = searcher('s.db')
# 	cur = s.con.execute('select * from urlcheck where rowid = %s' % url)
# 	for ii in cur.fetchmany():
# 		print(ii)