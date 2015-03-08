import gevent
from gevent.pool import Group


## Used for grouping greenlets

def talk(message):
	for i in xrange(3):
		print message 

g1 = gevent.spawn(talk, 'bar')
g2 = gevent.spawn(talk, 'foo')
g3 = gevent.spawn(talk, 'fizz')

group = Group()
group.add(g1)
group.add(g2)
group.join()

gevent.sleep(2)
print 'Added g3 into the group'
group.add(g3)
group.join()


## Used in the similar way as pool
from gevent import getcurrent

group = Group()

def hello_from(n):
	print 'Size of group %s' % len(group)
	print 'Hello from Greentlet %s' % id(getcurrent())

group.map(hello_from, xrange(3))


## ordered and unordered
def intensive(n):
	gevent.sleep(3-n)
	return 'task', n

print 'Ordered'

ogroup = Group()

for i in ogroup.imap(intensive, xrange(3)):
	print i

print 'Unordered'
ugroup = Group()

for i in ugroup.imap_unordered(intensive, xrange(3)):
	print i