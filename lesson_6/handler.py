
def handler(message, context):
    arg = message["body"]["arg"]
    print(arg)
    print(message["headers"])
    return {"result": arg * 2, "status": "noice"}

