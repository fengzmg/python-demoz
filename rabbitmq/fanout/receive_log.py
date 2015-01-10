import pika
import sys

exchange_name = 'logs'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name, type='fanout')
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange=exchange_name, queue=queue_name)

print '[*] Waiting for messages...    to exit press ctrl+c'

def callback(ch, method, properties, body):
    print "[x] Received %r" % body


channel.basic_consume(consumer_callback=callback, queue=queue_name, no_ack=True)

channel.start_consuming()