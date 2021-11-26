import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

from collections import defaultdict
from functools import partial

import docker

import uuid
import datetime


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
                "function_code": "def handler(message, context):\n    # your code here\n    return message",
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
# Key(EventType): Value(List[FunctionDefinition])
# EventType example "http|GET|/api/cats" it's a complex key
INSTANCES_DB = defaultdict(list) # gospadi prasti, act 2
# Key(EventType): Value(List[Dict[String, Any]]), for example {"trigger_time": <time>, "instance_id": <instance_id>}


app = FastAPI()


def _sanitize_record(record: dict, drop_fields: list):
    clean_record = record.copy()
    for field in drop_fields:
        if field in record:
            del clean_record[field]
    return clean_record


def sanitize(records: list[dict], fields=list[str]):
    return list(map(partial(_sanitize_record, drop_fields=fields), records))


@app.get("/functions")
def list_available_functions():
    global FUNCTIONS_DB
    response = {event_t: sanitize(function_defs, ["function_code"]) for event_t, function_defs in FUNCTIONS_DB.items()}
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

        command = f"sh -c 'PYTHONPATH=$PYTHONPATH:/tmp timeout {TIMEOUT} python -u runner.py'"

        environment = [f"HTTP_BODY={payload.http_body}",
                        f"HTTP_HEADER={payload.http_header}",
                        f"HTTP_VERB={payload.http_verb}",
                        f"HTTP_PATH={payload.http_path}",]

        resource_constraints = {"cpu_shares": 2, "mem_limit": "256mb", "pids_limit": 10}

        log_config = docker.types.LogConfig(type=docker.types.LogConfig.types.JSON, config={
                                              'max-size': '1g',
                                              'labels': 'production_status,geo'
                                            })

        configs = dict(
            stderr=True,
            stdout=True,
            # remove=True,
            detach=True,
            network="cloud_net",
            name=str(uuid.uuid4()),
            volumes=volumes,
            environment=environment,
            log_config=log_config
        )

        __container_ref = controller.containers.run("alexburlacu/functionsplatform:python-worker",
                                                    command,
                                                    **configs,
                                                    **resource_constraints)
        all_container_ids.append(configs["name"])
        INSTANCES_DB[key].append({"trigger_time": str(datetime.datetime.now()), "instance_id": configs["name"], "args": environment})

    return {"status": "ok", "container_ids": all_container_ids}


@app.get("/functions/instances")
def list_all_instances():
    global INSTANCES_DB
    response = {event_t: sanitize(instance_records, ["args"]) for event_t, instance_records in INSTANCES_DB.items()}
    return response


@app.get("/functions/instances/{instance_id}")
def lookup_specific_instance(instance_id: str = Path(...)):
    global INSTANCES_DB
    for event_t, instance_records in INSTANCES_DB.items():
        for record in instance_records:
            if record["instance_id"] == instance_id:
                return {"status": "ok", "event_type": event_t, **record}
    return {"status": "not_found"}


@app.get("/functions/instances/{instance_id}/logs")
def get_functions_instance_logs(instance_id: str = Path(...)):
    controller = docker.from_env()
    container = controller.containers.get(instance_id)
    return {"logs": str(container.logs())}
