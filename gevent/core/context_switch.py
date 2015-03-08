import gevent

def foo():
	print('running in foo')
	gevent.sleep(0)
	print('Explict context switch to foo again')


def bar():
	print('Explict context switch to bar')
	gevent.sleep(0)
	print('Implicit context switch back to bar')

gevent.joinall([gevent.spawn(foo), gevent.spawn(bar)])
