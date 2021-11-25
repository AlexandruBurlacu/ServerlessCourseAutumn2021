import os
import json

import pika

import handler # from /tmp/handler.py function

message_queue_uri = "message_queue" # because the container attaches to the network defined for data services

headers = {kv_pair.split(": ")[0]: kv_pair.split(": ")[1] for kv_pair in os.environ.get("HTTP_HEADER").splitlines()}
body = json.loads(os.environ.get("HTTP_BODY"))
path = os.environ.get("HTTP_PATH")
verb = os.environ.get("HTTP_VERB")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=message_queue_uri))
channel = connection.channel()
channel.queue_declare(queue=headers["X-Correlation-Id"])

message = {
    "headers": headers,
    "body": body["body"],
    "path": path,
    "verb": verb,
    "message_type": "http"
}

context = dict(message_queue_uri=message_queue_uri)

response = handler.handler(message, context)


channel.basic_publish(exchange='', routing_key=headers["X-Correlation-Id"], body=json.dumps(response)) # <- this response body, always make sure it's a str or bytes
connection.close()
