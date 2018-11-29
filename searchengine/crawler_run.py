#-*- encoding:utf-8 -*-
#!/usr/bin/env python

import multiprocessing as mp
import searchengine.crawler as crawl

crawler = crawl.crawler('searchindex.db')
sqlq = 'select url from urlcheck where indexed = "N" order by random() limit 5'

def work(link):
	res = None

	if terminating.is_set():
		return res

	try:
		if 'bkrs.info' in link and 'slovo' not in link:
			crawler.crawl(link)
	except KeyboardInterrupt:
		terminating.set()
	except Exception as e:
		res = str(e)

	return res


def initializer(_terminating):
	global terminating

	terminating = _terminating

def main(iter):
	terminating = mp.Event()

	PROCESSESS_COUNT = 5

	pool = mp.Pool(
		processes=PROCESSESS_COUNT,
		initializer=initializer,
		initargs=(terminating,)
	)

	try:
		data = pool.map(work, iter)
		pages = [i[0] for i in crawler.con.execute(sqlq).fetchall()]
		if len(pages) > 0:
			main(pages)

	except KeyboardInterrupt:
		pool.terminate()
		pool.join()
		raise


if __name__ == '__main__':
	page = 'https://bkrs.info/taolun/index.php'
	# page = 'https://bkrs.info/taolun/thread-309342.html'
	# crawler.createindextables(True)
	crawler.createindextables()
	pages = [i[0] for i in crawler.con.execute(sqlq).fetchall()]

	if len(pages) > 0:
		main(pages)
	else:
		main(crawler.crawl_init(page))