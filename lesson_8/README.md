# Serverless Course

## Lesson 8: Thinking about SLOs. Monitoring and Obvserability. Keeping latencies at bay.
- (8.1) What are SLI/SLO/SLA?
- (8.2) Monitoring. Tracing. Observability.
- (8.3) Keeping latencies at bay (Autoscaling, Hedged requests, Load shedding, Deadline propagation)

### Launching the system

In order to run this project you will need a fresh installation of Python, either standard or Anaconda, prefferably 3.10, because this version is used by the author, and `docker` and `docker-compose`.

For this version of the project, you don't need to pre-install the libraries which will be mounted into the functions anymore. Instead, go into `./docker` subdir and run `docker build -t alexburlacu/functionsplatform:python-worker .`.

Now, to launch the platform, first create a virtual environment, either using `conda` or `venv` and then install everything with `pip install -r requirements.txt`. After that, launch the data services specified in `docker-compose.yml` via `docker-compose up`. Then, run the `app.py` using `uvicorn`, like this:

```
uvicorn app:app
```

And finally, run `python gateway.py`. You're all set. Now I would recommend you play arround with it using `functionsplatform_cli.py` CLI and not bother using Swagger.


You can also see the Jaeger traces at `http://localhost:16686`. They will appear when your functions are triggered.


### API for adding tracing to a custom function

Example:
```python
from functionsplatform.sdk import tracing

# Message -|> dict
# Context -|> dict
# Return  -|> dict, but with key constraints
def handler(message, context):
    tracer = context.get("tracer")

    arg = message["body"]["arg"]
    print(arg)
    with tracing.span_from_context(tracer, context, name="print-headers") as span:
        tracing.set_attr(span, "special-attribute", "with-a-special-value")
        print(message["headers"])
    return {"result": arg * 2, "status": "noice"}
```

### Links about things mentioned during the lecture

#### SLI/SLO/SLA - the what, the how, the why?
- [An overview, from Atlassian](https://www.atlassian.com/itsm/service-request-management/slas)
- [A more in-depth analysis, from the SRE Book](https://sre.google/sre-book/service-level-objectives/)

#### Monitoring and Observability
- [A pretty detailed overview of Google's Monitoring System](https://sre.google/sre-book/monitoring-distributed-systems/)
- [About what observability trully means](https://softwareengineeringdaily.com/2021/02/04/debunking-the-three-pillars-of-observability-myth/), note that Cardinality means number of unique items
- [... and what should an observability system look at](https://medium.com/lightstephq/resources-and-transactions-a-fundamental-duality-in-observability-1035013bd66b)
- [Some guidance from MSDN](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/manage/monitor/observability)
- [And some sdk examples from AWS](https://docs.aws.amazon.com/lambda/latest/dg/python-tracing.html), for serverless platforms no less
- [The architecture of a typical tracing infrastructure with Jaeger](https://www.jaegertracing.io/docs/1.29/architecture/)


#### Strategies to reduce or otherwise bound the tail latencies in a distributed system
- [Load shedding and graceful degradation](https://sre.google/sre-book/addressing-cascading-failures/#xref_cascading-failure_load-shed-graceful-degredation)
- [More on load shedding](https://cloud.google.com/blog/products/gcp/using-load-shedding-to-survive-a-success-disaster-cre-life-lessons)
- [Deadline propagation](https://sre.google/sre-book/addressing-cascading-failures/#xref_cascading-failure_latency-and-deadlines)
- [About hedged requests strategy](https://courses.cs.duke.edu/cps296.4/fall13/838-CloudPapers/dean_longtail.pdf) which is a form of speculative execution, a must read IMO
- [A benchmark of latencies in serverless platforms](https://ease-lab.github.io/ease_website/pubs/STELLAR_ISWC21.pdf), it also outlines what are some common sources of these

- [An article on the cross-roads of SLOs and latency](https://robertovitillo.com/why-you-should-measure-tail-latencies/)
- [And a "war story" from WeaveWorks](https://www.weave.works/blog/a-tale-of-tail-latencies)

### Keywords
- [Firecraker VM](https://firecracker-microvm.github.io/)
- Multi-tenancy, see some patterns [here](https://docs.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns)
- [Sentry](https://docs.sentry.io/)
- Tail latency
- OpenTracing and OpenTelemetry



### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Collection" property="dct:title" rel="dct:type">Serverless Course Autumn 2021 - Lecture 8</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="alexandruburlacu.github.io" property="cc:attributionName" rel="cc:attributionURL">Alexandru Burlacu</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

