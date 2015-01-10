import pika
import sys

exchange_name = 'direct_logs'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name, type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello world'

channel.basic_publish(exchange=exchange_name,
                      routing_key=severity,
                      body=message)
print "[x] Sent %r:%r" % (severity, message)
connection.close()

