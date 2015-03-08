import gevent.monkey

gevent.monkey.patch_socket()

import gevent
import random
import urllib2
import simplejson as json

def task(pid):
	# gevent.sleep(random.randint(0,2)*0.01)
	response = urllib2.urlopen('http://json-time.appspot.com/time.json')
	result = response.read()

	json_result = json.loads(result)
	datetime = json_result['datetime']
	print "Task %s done: %s " % (pid, datetime)


def synchronous():
	for i in range(1, 10):
		task(i)

def asynchronous():
	threads = [gevent.spawn(task, i) for i in xrange(10)]
	gevent.joinall(threads)

print 'synchronous'
synchronous()

print 'asynchronous'
asynchronous()
