# event_type: HTTP_METHOD:/url/path

# MAP HTTP_METHOD URL to event_type

# MAKE ID -> event_type

# PUT in queue
# GET from queue by ID the response

import socket
import os
import pika
import json
import uuid
import time

import requests

# based on https://mleue.com/posts/simple-python-tcp-server/
from typing import Tuple, List, Callable
import socket
import threading
from httptools import HttpRequestParser
import http



class HttpRequestParserProtocol:
    def __init__(self, send_response: Callable):
		# we hand in and save a callback to be triggered once
		# we have received the entire request and can send a response
        self.send_response = send_response

    # parser callbacks
	# gets called once the start line is successfully parsed
    def on_url(self, url):
        print(f"Received url: {url}")
        self._url = url
        self._headers = []
        self._full_body = []

	# gets called on every header that is read from the request
    def on_header(self, name: bytes, value: bytes):
        print(f"Received header: ({name}, {value})")
        self._headers.append((name, value))

	# gets called continously while reading chunks of the body
    def on_body(self, body: bytes):
        print(f"Received body: {body}")
        self._full_body.append(body.decode("utf-8"))

	# gets called once the request was fully received and parsed
    def on_message_complete(self):
        print("Received request completely.")

        self._full_body = "".join(self._full_body)
        self.send_response()


def create_status_line(status_code: int = 200):
    code = str(status_code).encode()
    code_phrase = http.HTTPStatus(status_code).phrase.encode()
    return b"HTTP/1.1 " + code + b" " + code_phrase + b"\r\n"


def format_headers(headers: List[Tuple[bytes, bytes]]):
    return b"".join([key + b": " + value + b"\r\n" for key, value in headers])


def make_response(
    status_code: int = 200,
    headers: List[Tuple[bytes, bytes]] = None,
    body: bytes = b"",
):
    if headers is None:
        headers = []
    if body:
		# if you add a body you must always send a header that informs
		# about the number of bytes to expect in the body
        headers.append((b"Content-Length", str(len(body)).encode("utf-8")))
    content = [
        create_status_line(status_code),
        format_headers(headers),
        b"\r\n" if body else b"",
        body,
    ]
    return b"".join(content)


class Session:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.response_sent = False
        self.protocol = HttpRequestParserProtocol(self.send_response)
        self.parser = HttpRequestParser(self.protocol)

    def run(self):
        while True:
            if self.response_sent:
                break
            data = self.client_socket.recv(1024)
            print(f"Received {data}")
            self.parser.feed_data(data)
        self.client_socket.close()
        print(f"Socket with {self.address} closed.")


    def send_request(self):
        http_path = self.protocol._url.decode("utf-8")
        body = self.protocol._full_body
        header = self.protocol._headers
        corr_id = uuid.uuid4()
        header.append(("X-Correlation-Id", corr_id))

        serialized_header = "\n".join(f"{str(k)}: {str(v)}" for k, v in header)

        print(self.parser.get_method())
        print(http_path)

        response = requests.post("http://localhost:8000/functions/trigger",
                                    headers={"Content-Type": "application/json"},
                                    data=json.dumps({"http_body": json.dumps({"body": json.loads(body)},
                                                                                default=lambda x: x.decode("utf-8")) if body else "",
                                                    "http_header": serialized_header,
                                                    "http_path": http_path,
                                                    "http_verb": self.parser.get_method().decode()}))
        response_bodies = response.json().get("container_ids")

        print(response_bodies)

        return corr_id, response_bodies[0] if len(response_bodies) > 0 else None
    
    def get_response(self, corr_id):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=f"{corr_id}")
        for step in range(1, 7):
            try:
                method_frame, header_frame, body = channel.basic_get(f"{corr_id}")
                if method_frame:
                    print(method_frame, header_frame, body)
                    channel.basic_ack(method_frame.delivery_tag)
                    return body, []
                else:
                    time.sleep(0.2 * 2 ** step)
            except Exception:
                print(f"Error # {step}")
                time.sleep(0.25 * 2 ** step)

        return b"Response timeout", []


    def send_response(self):
        # trigger/send to serverless instance
        corr_id, instance_id = self.send_request()

        headers = [(b"X-Serverless-Instance-Id", f"{instance_id}".encode())]

        if instance_id:
            print(f"Successfully triggered {instance_id}")
            body, new_headers = self.get_response(corr_id)
            headers.extend(new_headers)
            print(body)
        else:
            body = b""

        response = make_response(status_code=200, headers=headers, body=body)
        self.client_socket.send(response)
        print("Response sent.")
        self.response_sent = True


def serve_forever(host: str, port: int):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Socket established with {address}.")
        session = Session(client_socket, address)
        t = threading.Thread(target=session.run)
        t.start()


if __name__ == "__main__":
    serve_forever("0.0.0.0", 5000)