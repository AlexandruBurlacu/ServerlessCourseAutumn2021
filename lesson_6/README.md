# Lesson 6


## SDK Components
- CLI tool to CRUD/test-run functions
- API for more conveninent writing of functions (less boilerplate)
- Allow for reading function execution logs
- [Later] Observability instrumentation (metrics, log collection, tracing support)
- [Maybe] Some End-to-End tests

### Launching the system

In order to run this project you will need a fresh installation of Python, either standard or Anaconda, prefferably 3.10, because this version is used by the author, and `docker` and `docker-compose`.

For this version of the project, you don't need to pre-install the libraries which will be mounted into the functions anymore. Instead, go into `./docker` subdir and run `docker build -t alexburlacu/functionsplatform:python-worker`.

Now, to launch the platform, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`. After that, launch the data services specified in `docker-compose.yml` via `docker-compose up`. Then, run the `app.py` using `uvicorn`, like this:

```
uvicorn app:app
```

And finally, run `python gateway.py`. You're all set. Now I would recommend you play arround with it using `functionsplatform.py` CLI and not bother using Swagger.



### CLI tool to CRUD/test-run functions

```
COMMANDs:
  create
  list
  delete
  trigger
  logs
  list-instances
  lookup-instance

OPTIONs:
  --help        global help
  --verbose
  --version
  --show-help   per-command help

Example:
  functionsplatform create --http-verb=GET --http-path=/api/cats  --code-file handler.py --name some_name
  functionsplatform list [--filter=glob_patter]
  functionsplatform logs some_instance_id
```

### API for more conveninent writing of functions (less boilerplate)

Example:
```python
from functionsplatform.sdk import log, trace_function, ...

# Message -|> dict
# Context -|> dict
# Return  -|> dict, but with key constraints

def handle(message: Message, context: Message) -> Return:
    # some business logic
    return {"something": of_value}
```

## Links about DX

#### Documentation
- A way to document architecture decisions [can be found here](https://adr.github.io/)
- [FastAPI](https://fastapi.tiangolo.com/) and [Connexion](https://connexion.readthedocs.io/en/stable/quickstart.html) are two different ways how to keep documentation in sync with the actual code.
- During the lecture we mentioned Confluent, Wiki and the use of formus, a some free Open Source projects being are Talkyard and Discourse, but some even use dedicated Slack organizations for this.
- HATEOAS implemented in not just [one](https://jsonapi.org/), or [two](https://stackoverflow.com/questions/25819477/relationship-and-difference-between-hal-and-hateoas#25819578), but [three](https://developer.paypal.com/docs/api/reference/api-responses/#hateoas-links) ways.


#### API Design
- [Apigee REST API design guidelines](https://cloud.google.com/files/apigee/apigee-web-api-design-the-missing-link-ebook.pdf)
- [Google's Web API design guidelines](http://apistylebook.com/design/guidelines/google-api-design-guide)
- If you're interested in library API design, [here's a good resource on it](https://github.com/papers-we-love/papers-we-love/blob/master/api_design/api-design.pdf)
- [How to design a good API and why it matters](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/32713.pdf) by Joshua Bloch @ Google

#### Error messages
- [From UX perspective](https://cxl.com/blog/error-messages/)
- [About Error codes](https://softwareengineering.stackexchange.com/questions/209693/best-practices-to-create-error-codes-pattern-for-an-enterprise-project)
- [Best practices with examples of how to handle HTTP API Errors](https://nordicapis.com/best-practices-api-error-handling/)

Covering both error messages and API design, [a primer from Keras](https://blog.keras.io/category/essays.html), a deep learning library.

#### Misc and mentions
- We mentioned APL during the lecture, maybe you would want to try it, [here](https://tryapl.org/)

### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 6</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

