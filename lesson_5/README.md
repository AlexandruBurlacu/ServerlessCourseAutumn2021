# Serverless Course

## Lesson 5: Finishing what we started last time + reducing latencies in the system

- (5.0) Improving the system: reducing startup time and increasing hardware utilization.
- (5.1) Timeouts
- (5.2) Make it run async
- (5.3) Cold start problem. Hot vs Cold latency
- (5.4) Environment reuse
- (5.5) Application-level tricks


In order to run this project you will need a fresh installation of Python, either standard or Anaconda, prefferably 3.10, because this version is used by the author, and `docker` and `docker-compose`.

You will need to pre-install the libraries which will be mounted into the functions. For this, please create a special virtual environment via `python3.10 -m venv .functions_venv` and once done, enter it and install the necessary libraries via `pip install -r requirements.functions.txt`.

Now, to launch the platform, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`. After that, launch the data services specified in `docker-compose.yml` via `docker-compose up`. Then, run the `app.py` using `uvicorn`, like this:

```
uvicorn app:app
```

And finally, run `python gateway.py`. You're all set.

The API Gateway (`gateway.py`) and the Serverless Platform (`app.py`) are not part of the `docker-compose.yml` because of 2 reasons:
1. `app.py` has to interact with the `docker` daemon and specify volumes, which can get very tricky if used from within docker-compose
2. They change much faster during current development, and continiously restarting these is cumbersome


## Example workflow

You can play around with the API Gateway + Serverless Platform via Swagger at `localhost:8000/docs` or using `curl`.

A basic workflow would be:
1. Define a serverless function with `POST /functions`
```bash
curl -X 'POST' \
  'http://localhost:8000/functions' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_type": "http|GET|/request/to/github",
  "function_code": "import urllib.request\nwith urllib.request.urlopen('\''http://www.python.org/'\'') as f:\n    print(f.read().decode('\''utf-8'\''))",
  "function_name": "github_request"
}'
```
2. List available serverless functions with `GET /functions`
```bash
curl 'http://localhost:8000/functions'
```
3. Finally, trigger a function execution via the API Gateway.
```bash
curl 'http://localhost:5000/request/to/github'
```

Notice that you won't see the output, but if you check server logs of both `app.py` and `gateway.py` you will notice that the provisioning and execution were successful.
But how do we get the response from such a function?

## Getting back a response

You will have to define your function using the following template:

```python
import os
import json

import pika

# <add your libraries here>

message_queue_uri = "message_queue" # because the container attaches to the network defined for data services

headers = {kv_pair.split(": ")[0]: kv_pair.split(": ")[1] for kv_pair in os.environ.get("HTTP_HEADER").splitlines()}
body = json.loads(os.environ.get("HTTP_BODY"))
path = os.environ.get("HTTP_PATH")
verb = os.environ.get("HTTP_VERB")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=message_queue_uri))
channel = connection.channel()
channel.queue_declare(queue=headers["X-Correlation-Id"])


##########################
#   add your code here   #
#  *define response body #
##########################


channel.basic_publish(exchange='', routing_key=headers["X-Correlation-Id"], body=json.dumps(body)) # <- this response body, always make sure it's a str or bytes
connection.close()
```

For example, a complete function creation request:
```bash
curl -X 'POST' \
  'http://localhost:8000/functions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_type": "http|POST|/echo",
  "function_code": "import os\nimport json\n\nimport pika\n\n# <add your libraries here>\n\nmessage_queue_uri = \"message_queue\"\n\nheaders = {kv_pair.split(\": \")[0]: kv_pair.split(\": \")[1] for kv_pair in os.environ.get(\"HTTP_HEADER\").splitlines()}\nbody = json.loads(os.environ.get(\"HTTP_BODY\"))\npath = os.environ.get(\"HTTP_PATH\")\nverb = os.environ.get(\"HTTP_VERB\")\n\nconnection = pika.BlockingConnection(\n    pika.ConnectionParameters(host=message_queue_uri))\nchannel = connection.channel()\nchannel.queue_declare(queue=headers[\"X-Correlation-Id\"])\n\n\n##########################\n#   add your code here   #\n#  *define response body #\n##########################\n\n\nchannel.basic_publish(exchange='\'''\'', routing_key=headers[\"X-Correlation-Id\"], body=json.dumps(body)) # <- this response body\nconnection.close()\n",
  "function_name": "echo"
}'
```

If you then call `curl -v -XPOST -d '{"Hello": "Valera"}' -H 'Content-Type: application/json' http://localhost:5000/echo` the response should be `{"body": {"Hello": "Valera"}}`.



## Links

- [The code written during the lecture](https://github.com/AlexandruBurlacu/ServerlessCourseAutumn2021/tree/lesson-5-it-works-but-no-libs)
- Gatway is based on the code from [this blogpost](https://mleue.com/posts/simple-python-tcp-server/)
- [Some optimizations for a serverless platform](https://tomasz.janczuk.org/2018/03/how-to-build-your-own-serverless-platform.html), the second half of the article


### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 5</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

