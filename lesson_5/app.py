import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

from collections import defaultdict
from functools import partial

import docker

import uuid


TIMEOUT = 60 # seconds


EventType = str # EventType example "http|GET|/api/cats" it's a complex key
Code = str

class FunctionDefinition(BaseModel):
    event_type: EventType
    function_code: Code # in DB it's a path
    function_name: str
    # function_owner

    @staticmethod
    def example():
        return {
                "event_type": "http|GET|/api/cats",
                "function_code": "import this",
                "function_name": "calling_cats_not"
                }


Header = str
Body = str
Path = str
Verb = str

class HttpEventPayload(BaseModel):
    http_header: Header
    http_body: Body
    http_path: Path
    http_verb: Verb

    @staticmethod
    def example():
        return {
                "http_header": "Content-Type: text/plain\nX-Special-Header: i-think-they-are-deprecated",
                "http_body": "See also: https://stackoverflow.com/questions/3561381/custom-http-headers-naming-conventions, anyway, show us cats!",
                "http_path": "/api/cats",
                "http_verb": "GET"
                }



CODE_REPO_PATH = "code_repo/"
FUNCTIONS_DB = defaultdict(list) # gospadi prasti
# EventType: List[FunctionDefinition]
# EventType example "http|GET|/api/cats" it's a complex key


app = FastAPI()



def _sanitize_function_def(func_def: dict, drop_fields: list):
    clean_func_def = func_def.copy()
    for field in drop_fields:
        if field in func_def:
            del clean_func_def[field]
    return clean_func_def


def sanitize(function_defs: list[dict]):
    return list(map(partial(_sanitize_function_def, drop_fields=["function_code"]), function_defs))


@app.get("/functions")
def list_available_functions():
    global FUNCTIONS_DB
    response = {event_t: sanitize(function_defs) for event_t, function_defs in FUNCTIONS_DB.items()}
    return response


def handle_code(function_key, function_code, function_name):
    code_type = function_key.replace('|', "__").replace("/", "---") # http|GET|/api/cats -> http__GET__---api---cats
    function_code_dir = f"{os.path.join(CODE_REPO_PATH, code_type)}"

    os.makedirs(function_code_dir, exist_ok=True)

    function_code_path = os.path.join(function_code_dir, f"{function_name}.py")
    with open(function_code_path, "w") as fptr:
        fptr.write(function_code)

    return f"{os.path.join(code_type, function_name)}.py"


@app.post("/functions")
def create_function(func_def: FunctionDefinition = FunctionDefinition.example()):
    global FUNCTIONS_DB
    key = func_def.event_type
    
    func_def_dict = func_def.dict()
    func_def_dict["function_code"] = handle_code(key, func_def.function_code, func_def.function_name)

    FUNCTIONS_DB[key].append(func_def_dict)
    return {"status": "ok"}


@app.delete("/functions/{function_name}")
def delete_function(function_name: str = "calling_cats_not"):
    for event_t, func_defs in FUNCTIONS_DB.items():
        for idx, func_def in enumerate(func_defs):
            if func_def["function_name"] == function_name:
                del FUNCTIONS_DB[event_t][idx]
        
    return {"status": "ok"}



def make_key_from_payload(payload: dict):
    return f"http|{payload.get('http_verb')}|{payload.get('http_path')}"


@app.post("/functions/trigger")
def trigger_functions_execution(payload: HttpEventPayload = HttpEventPayload.example()):
    global FUNCTIONS_DB
    controller = docker.from_env()

    key = make_key_from_payload(payload.dict())

    all_container_ids = []
    for function in FUNCTIONS_DB.get(key, []):
        f_code_path = function.get("function_code")

        volumes = {os.path.join(os.getcwd(), CODE_REPO_PATH, f_code_path): {
                            "bind": "/tmp/handler.py",
                            "mode": "ro"}}

        command = f"timeout {TIMEOUT} python -u /tmp/handler.py"

        environment = [f"HTTP_BODY={payload.http_body}",
                        f"HTTP_HEADER={payload.http_header}",
                        f"HTTP_VERB={payload.http_verb}",
                        f"HTTP_PATH={payload.http_path}",]

        configs = dict(
            stderr=True,
            stdout=True,
            remove=True,
            detach=True,
            name=str(uuid.uuid4()),
            volumes=volumes,
            environment=environment
        )

        container_ref = controller.containers.run("python:3.8-slim", command, **configs)
        all_container_ids.append(configs["name"])

    return {"status": "ok", "container_ids": all_container_ids}



# @app.get("/functions/instances/{instance_id}")