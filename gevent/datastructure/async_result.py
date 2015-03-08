import gevent
from gevent.event import AsyncResult
a = AsyncResult()

def setter():
	gevent.sleep(3) # block for 3 seconds
	a.set('Hello!')

def waiter():
	print 'Trying to get the result from a..'
	print a.get()


gevent.joinall([
	gevent.spawn(setter), 
	gevent.spawn(waiter)]
	)