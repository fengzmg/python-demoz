import time
import gevent
from gevent import select

start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)

def gr1():
	print '[GR1] Started Polling: %s' % tic()
	select.select([],[],[], 2)
	print '[GR1] End Polling: %s' % tic()

def gr2():
	print '[GR2] Started Polling: %s' % tic()
	select.select([],[],[], 2)
	print '[GR2] End Polling: %s' % tic()

def gr3():
	print '[GR3] Started Polling: %s' % tic()
	select.select([],[],[], 2)
	print '[GR3] End Polling: %s' % tic()

def gr4():
	print "Let's do something while the others are polling..%s" % tic()
	gevent.sleep(1)

gevent.joinall([gevent.spawn(gr1), gevent.spawn(gr2), gevent.spawn(gr3), gevent.spawn(gr4)])