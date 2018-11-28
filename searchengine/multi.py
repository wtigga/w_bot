#-*- encoding:utf-8 -*-
#!/usr/bin/env python

import multiprocessing as mp
import searchengine.search as crawl

crawler = crawl.crawler('searchindex.db')

def work(link):
	res = None

	if terminating.is_set():
		return res

	try:
		# crawler.import_test()
		if 'bkrs.info' in link:
			# print('worker url is ', link)
			crawler.crawl([link], 1)
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


	PROCESSESS_COUNT = 20

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
	crawler.createindextables(True)
	# crawler.createindextables()
	main(crawler.crawl_init(page))
