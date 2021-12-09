from functionsplatform.sdk import tracing

def handler(message, context):
    tracer = context.get("tracer")

    arg = message["body"]["arg"]
    print(arg)
    with tracing.span_from_context(tracer, context, name="print-headers") as span:
        tracing.set_attr(span, "special-attribute", "with-a-special-value")
        print(message["headers"])
    return {"result": arg * 2, "status": "noice"}

