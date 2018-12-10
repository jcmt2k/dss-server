#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channelReceive = connection.channel()
channelReceive.queue_declare(queue='StorageRequests')

channelSend = connection.channel()
channelSend.queue_declare(queue='StorageResponses')

def callbackReceive(ch, method, properties, body):
  print(" Received %r" % body)
  channelSend.basic_publish(exchange='',
          routing_key='StorageResponses',
          body="respuesta a: %r" % body)


channelReceive.basic_consume(callbackReceive,
        queue='StorageRequests',
        no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channelReceive.start_consuming()

