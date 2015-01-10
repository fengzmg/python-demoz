import pika
import time

queue_name = 'task_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)

print '[*] Waiting for messages...    to exit press ctrl+c'

def callback(ch, method, properties, body):
    print "[x] Received %r" % body
    time.sleep(body.count('.'))
    print '[x] Done'
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(consumer_callback=callback, queue=queue_name)

channel.start_consuming()