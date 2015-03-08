import gevent
from gevent.queue import Queue

tasks = Queue() # this is similar to java blockingqueue

def worker(n):
	while not tasks.empty():
		print 'worker %s is asking for job' % n
		task = tasks.get()
		print 'worker %s got task %s' % (n, task)
		gevent.sleep(0)

	print 'All work are done. Quit time'

def master():
	gevent.sleep(2)
	[tasks.put_nowait(i) for i in xrange(1, 2500)]


gevent.spawn(master).join()

gevent.joinall([
	gevent.spawn(worker, 'steve'),
	gevent.spawn(worker, 'john'),
	gevent.spawn(worker, 'michelle'),
	gevent.spawn(worker, 'stania'),
	])
