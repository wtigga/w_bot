#-*- encoding:utf-8 -*-
#!/usr/bin/env python

import multiprocessing as mp
import searchengine.crawler as crawl

crawler = crawl.crawler('searchindex.db')

def work(link):
	res = None

	if terminating.is_set():
		return res

	try:
		if 'bkrs.info' in link:
			crawler.crawl([link])
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
		# return data
	except KeyboardInterrupt:
		pool.terminate()
		pool.join()
		raise


if __name__ == '__main__':
	page = 'https://bkrs.info/taolun/index.php'
	# page = 'https://bkrs.info/taolun/thread-309342.html'
	# crawler.createindextables(True)
	crawler.createindextables()
	# crawler.con.execute('create table if not exists urls(url unique, text, indexed)')
	# crawler.con.commit()
	main(crawler.crawl_init(page))
