from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

import json


app = FastAPI()
db = dict()


class WebHookEvent(BaseModel):
    event: str
    time: str


@app.get("/events-so-far")
async def root():
    global db
    data = []
    for key in db.keys():
        data.append(db.get(key))
    return {"data": data}


@app.post("/webhook")
async def register(event: WebHookEvent):
    global db
    data = jsonable_encoder(event)
    db[f"{data}"] = data
    return {"status": "ok"}