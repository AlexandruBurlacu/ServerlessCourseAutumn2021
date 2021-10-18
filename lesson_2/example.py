def handler(request, context, return_callback):
    """
    A generic handler for FaaS can look something like this

    request: can keep information about specific request/event message to which the function has to react in some way
    context: system specific context, can keep information about available libs, environment variables, or other stuff
    retur_callback: a function which is part of the platform API, which will forward the return value back to the caller of this function
    """
    # do something useful
    # return something_useful
    something_useful = NotImplemented()
    return_callback(something_useful)
