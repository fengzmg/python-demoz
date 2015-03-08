import gevent
from gevent.pool import Pool

pool = Pool(2)

def hello_from(n):
	print 'size of the pool: %d' % len(pool)

pool.map(hello_from, xrange(3))


## Usage example

class SocketPool(object):
	def __init__(self):
		self.pool = Pool(800)
		self.pool.start()

	def listen(self, socket):
		while True:
			socket.recv()

	def add_handler(self, socket):
		if self.pool.full():
			raise Exception('At maximum pool size')
		else:
			self.pool.spawn(self.listen, socket)

	def shutdonw(self):
		self.pool.kill()