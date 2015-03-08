import gevent

def win():
	return 'you win'

def fail():
	raise Exception('You fail at faling')

winner = gevent.spawn(win)
loser = gevent.spawn(fail)

print 'winner.started = ', winner.started
print 'loser.started = ', loser.started

# Exception thrown in greenlet stays in greenlet
try:
	gevent.joinall([winner, loser])
except Exception as e:
	print 'This will never be reached'

print 'winner.value = ', winner.value
print 'loser.value = ', loser.value

print 'winner.ready = ', winner.ready()
print 'loser.ready = ', loser.ready()

print 'winner.successful = ', winner.successful()
print 'loser.successful = ', loser.successful()

# The exception raised in fail, will not propagate outside the
# greenlet. A stack trace will be printed to stdout but it
# will not unwind the stack of the parent.

print(loser.exception)

# It is possible though to raise the exception again outside
# raise loser.exception
# or with
# loser.get()