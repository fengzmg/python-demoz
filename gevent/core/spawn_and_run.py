import gevent
from gevent import Greenlet

def foo(message, n):
	gevent.sleep(n)
	print message

# Initialize a new Greenlet instance running the named function
thread1 = Greenlet.spawn(foo, "hello from Greenlet instance", 2)

# using the gevent wrapper for starting a new greenlet
thread2 = gevent.spawn(foo, "hello from wrapper", 2)

# lambda expression can be used 
thread3 = gevent.spawn(lambda x: x+1, 2)

threads = [thread1, thread2, thread3]

gevent.joinall(threads)


## Extend the Greenlet class

class MyGreenlet(Greenlet):
	def __init__(self, message, n):
		Greenlet.__init__(self)
		self.message = message
		self.n = n

	def _run(self):
		print self.message
		gevent.sleep(self.n)


g = MyGreenlet("Hi there", 3)
g.start()
g.join()



