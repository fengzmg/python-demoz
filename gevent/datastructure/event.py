import gevent
from gevent.event import Event

evt = Event()

def setter():
	print 'A: Hey wait for me, I have to do something'
	gevent.sleep(3)
	print 'Ok. I am done'
	evt.set()  # wake up other when done

def waiter():
	print 'I will wait for you'
	evt.wait()
	print 'Ok. Let go together'


gevent.joinall([
	gevent.spawn(setter),
	gevent.spawn(waiter),
	gevent.spawn(waiter),
	gevent.spawn(waiter),
	gevent.spawn(waiter),
	gevent.spawn(waiter),
	gevent.spawn(waiter),
	])