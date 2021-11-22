# Lesson 6


## SDK Components
- CLI tool to CRUD/test-run functions
- API for more conveninent writing of functions (less boilerplate)
- Allow for reading function execution logs
- [Later] Observability instrumentation (metrics, log collection, tracing support)
- [Maybe] Some End-to-End tests

### CLI tool to CRUD/test-run functions

Use `argparse`:
```
functionsplatform OPERATION [--OPTIONS|-O]
  create
  list
  delete
  trigger
  logs
  list-instances
  help

Example:
  functionsplatform create --event-type=http|GET|/api/cats  [--from-file handler.py|--from-stream -] --name some_name
  functionsplatform list --all|--filter
  functionsplatform logs --instance-id=some_id --tail=100 --stderr
```

### API for more conveninent writing of functions (less boilerplate)

Example:
```python
from functionsplatform.sdk import log, trace_function, ...

# Message -|> dict
# Context -|> dict
# Return -|> dict, but with key constraints

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

#### Misc and mentions
- We mentioned APL during the lecture, maybe you would want to try it, [here](https://tryapl.org/)

