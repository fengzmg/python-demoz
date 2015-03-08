import gevent
from gevent import sleep
from gevent.pool import Pool
from gevent.coros import BoundedSemaphore

sem = BoundedSemaphore(2)

def worker1(n):
	sem.acquire()
	print 'Worker %s accquired lock' % n
	sleep(1)
	sem.release()
	print 'Worker %s released lock' % n

def worker2(n):
	with sem:
		print 'Worker %s accquired lock' % n
		sleep(1)
	print 'Worker %s released lock' % n

pool = Pool()
pool.map(worker1, xrange(0, 5))
pool.map(worker2, xrange(5, 10))
