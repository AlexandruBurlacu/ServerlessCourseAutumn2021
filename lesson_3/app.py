import os
from fastapi import FastAPI
from pydantic import BaseModel

from collections import defaultdict

import docker


code_repo_path = "code_repo/"
functions_db = defaultdict(list) # gospadi prasti
# EventType: List[FunctionDefinition]
# EventType example "http|GET|/api/cats" it's a complex key


app = FastAPI()

EventType = str # Enum
Code = str

class FunctionDefinition(BaseModel):
    event_type: EventType
    function_code: Code # in DB it's a path
    function_name: str
    # function_owner




@app.get("/functions")
def list_available_functions():
    global functions_db
    return functions_db # TODO: remove function_code path from response


def handle_code(function_key, function_code, function_name):
    code_type = function_key.replace('|', "__").replace("/", "---") # http|GET|/api/cats -> http__GET__---api---cats
    function_code_dir = f"{os.path.join(code_repo_path, code_type)}"

    os.makedirs(function_code_dir, exist_ok=True)

    function_code_path = os.path.join(function_code_dir, f"{function_name}.py")
    with open(function_code_path, "w") as fptr:
        fptr.write(function_code)

    return function_code_path


@app.post("/functions")
def create_function(func_def: FunctionDefinition):
    global functions_db
    key = func_def.event_type

    function_code_path = handle_code(key, func_def.function_code, func_def.function_name)
    
    func_def_dict = func_def.dict()
    func_def_dict["function_code"] = function_code_path

    functions_db[key].append(func_def_dict)
    return {"status": "ok"}


@app.delete("/functions/:function_name") # TODO
def delete_function(function_name: str):
    # for event_t, func_defs in functions_db.items():
        
    return {"status": "ok"}


Header = str
Body = str
Path = str
Verb = str

class HttpEventPayload(BaseModel):
    http_header: Header
    http_body: Body
    http_path: Path
    http_verb: Verb


def make_key_from_payload(payload: dict):
    return f"http|{payload.get('http_verb')}|{payload.get('http_path')}"


@app.post("/functions/trigger")
def trigger_functions_execution(payload: HttpEventPayload):
    global functions_db
    controller = docker.from_env()

    key = make_key_from_payload(payload.dict())

    all_logs = []
    for function in functions_db.get(key, []):
        f_name = function.get("function_name")
        f_code_path = function.get("function_code")

        logs = controller.containers.run("python:3.8-slim", f"python {os.path.join('/tmp/', f_code_path)}",
                                        volumes={os.path.join(os.getcwd(), code_repo_path): {
                                                        "bind": os.path.join("/tmp/", code_repo_path),
                                                        "mode": "ro"}})
        all_logs.append(logs)

    return {"status": "ok", "all_logs": all_logs}

