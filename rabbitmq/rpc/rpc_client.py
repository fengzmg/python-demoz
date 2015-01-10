#!usr/bin/env python
import pika
import uuid
import sys

class FibRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, queue=self.callback_queue, no_ack=True)

    def on_response(self, ch, method, props, body):
        print '[.] Received response with correlation_id %s' % props.correlation_id
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(correlation_id=self.correlation_id,
                                                                   reply_to=self.callback_queue),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)



fib_rpc = FibRpcClient()

n = int(sys.argv[1]) or 30
print '[x] Requesting fib(%s)' % n
response = fib_rpc.call(n)

print '[.] Got %r' % response