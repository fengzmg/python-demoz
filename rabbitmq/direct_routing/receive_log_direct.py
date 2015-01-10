import pika
import sys

exchange_name = 'direct_logs'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name, type='direct')
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

severities = sys.argv[1:]

if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % sys.argv[0]
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=severity)


print '[*] Waiting for logs...    to exit press ctrl+c'

def callback(ch, method, properties, body):
    print "[x] Received %r:%r" % (method.routing_key, body)


channel.basic_consume(consumer_callback=callback, queue=queue_name, no_ack=True)

channel.start_consuming()