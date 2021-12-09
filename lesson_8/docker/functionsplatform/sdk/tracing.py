from contextlib import contextmanager
import json

from opentelemetry import trace, propagators
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.exporter.jaeger import JaegerSpanExporter


def _is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False



def set_attr(span, key, value):
    span.set_attribute(key, json.dumps(value) if _is_jsonable(value) else str(value))


@contextmanager
def span_from_context(tracer, context, *, name="span-in-custom-handler"):
    with tracer.use_span(context.get("tracing_context")) as outer_span:
        with tracer.start_as_current_span(name) as span:
            yield span

@contextmanager
def start_span(tracer, name):
    with tracer.start_as_current_span(name) as span:
        yield span


@contextmanager
def outbound_trace(url, headers):
    span = trace.get_current_span()
    span.set_attribute("destination.url", url)

    propagators.inject(dict.__setitem__, headers)

    yield span, headers


@contextmanager
def inbound_trace(tracer, headers, name):
    inbound_span = propagators.extract(
            propagators.textmap.DictGetter(), headers)["current-span"]
    with tracer.use_span(inbound_span):
        with tracer.start_as_current_span(name) as span:
            yield span


def init_tracer(service_name, collector_endpoint_host="jaeger"):
    trace.set_tracer_provider(TracerProvider())

    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(JaegerSpanExporter(
            service_name=service_name,
            # configure agent
            #agent_host_name='jaeger-agent',
            #agent_port=6831,
            # optional: configure also collector
            collector_endpoint = f'http://{collector_endpoint_host}:14268/api/traces?format=jaeger.thrift',
            # collector_protocol='http',
            # username=xxxx, # optional
            # password=xxxx, # optional
        ))
    )

    return trace.get_tracer(service_name)