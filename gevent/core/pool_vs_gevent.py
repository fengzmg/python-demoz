import time

def echo(i):
	time.sleep(0.01)
	return i

# Non determinstic Process Pool
from multiprocessing.pool import Pool

p = Pool(10)
run1 = [a for a in p.imap_unordered(echo, xrange(10))]
run2 = [a for a in p.imap_unordered(echo, xrange(10))]
run3 = [a for a in p.imap_unordered(echo, xrange(10))]
run4 = [a for a in p.imap_unordered(echo, xrange(10))]

print run1
print run2
print run3
print run4

print 'multiprocessing.pool List are equal?', run1 == run2 == run3 == run4

from gevent.pool import Pool

p = Pool(10)

run1 = [a for a in p.imap_unordered(echo, xrange(10))]
run2 = [a for a in p.imap_unordered(echo, xrange(10))]
run3 = [a for a in p.imap_unordered(echo, xrange(10))]
run4 = [a for a in p.imap_unordered(echo, xrange(10))]

print run1
print run2
print run3
print run4

print 'gevent.pool List are equal?', run1 == run2 == run3 == run4
