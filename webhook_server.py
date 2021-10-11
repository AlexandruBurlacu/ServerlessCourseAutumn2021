from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from enum import Enum

import datetime
import requests

import json

app = FastAPI()
db = dict()


class Event(Enum):
    CREATED_EVENT = 0
    DELETED_EVENT = 1
    LISTED_EVENT = 2


class WebHookRegistration(BaseModel):
    username: str
    subscriber_url: str
    registration_name: str
    event_type: Event


class DummyEntity(BaseModel):
    token: str


entities = [DummyEntity(token="123"), DummyEntity(token="233"), DummyEntity(token="128423")]


@app.get("/status") # healthcheck
async def root():
    return {"status": "up"}


def broadcast_event(event_type: Event):
    global db
    for key in db.keys():
        wh_reg = db.get(key)
        if event_type.value == wh_reg["event_type"]:
            requests.post(wh_reg['subscriber_url'], data=json.dumps({"event": f"{wh_reg['event_type']}", "time": f"{datetime.datetime.now()}"}))


@app.get("/entity/list")
async def list_entities():
    broadcast_event(Event.LISTED_EVENT)
    return entities


@app.delete("/entity/:entity_id")
async def delete_entity(entity_id: str):
    broadcast_event(Event.DELETED_EVENT)
    global entities
    try:
        entities.remove(DummyEntity(token=entity_id))
        return {"status": "ok"}
    except Exception as error:
        return {"status": "already removed"}
        


@app.post("/entity")
async def create_entity(entity: DummyEntity):
    broadcast_event(Event.CREATED_EVENT)
    global entities
    value = jsonable_encoder(entity)
    entities.append(value)
    return {"status": "ok"}


@app.get("/webhook") # Read(All)
async def event_trigger():
    global db
    return {"registrations": [{"key": key, "value": db.get(key)} for key in db.keys()]}


@app.get("/webhook/:key") # Read(One)
async def event_trigger(key: str):
    global db
    return {"registration": {"key": key, "value": db.get(key)}}


@app.delete("/webhook/:key") # Delete
async def event_trigger(key: str):
    global db
    resp = {"status": "deleted", "deleted_entry": {"key": key, "value": db.get(key)}}
    del db[key]
    return resp


@app.post("/webhook") # Create
async def register(registration: WebHookRegistration):
    global db
    key = f"{registration.username}:{registration.registration_name}"
    value = jsonable_encoder(registration)
    db[key] = value
    return {"status": "ok"}

