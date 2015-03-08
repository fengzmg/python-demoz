import gevent
from gevent import Timeout

seconds = 10

## Explicly start the timeout
timeout = Timeout(seconds)
timeout.start()

def wait():
	gevent.sleep(10)

try:
	gevent.spawn(wait).join()
except Timeout:
	print 'Could not complete'

## Using timeout Context Manager
time_to_wait = 5

class TooLong(Exception):
	pass

try:
	with Timeout(time_to_wait, TooLong):
		gevent.sleep(10)
except TooLong:
	print 'Timeout of TooLong'

## Use gevent timeout arguments

def wait_again():
	gevent.sleep(2)

timer = Timeout(1).start()

thread1 = gevent.spawn(wait_again)

try:
	thread1.join(timeout=timer) # as argument of join()
except Timeout:
	print 'Thread 1 timeout'

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait_again)

try:
	thread2.get(timeout=timer)
except Timeout:
	print 'Thread 2 timeout'

